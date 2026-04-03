from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 条件导入openai（仅在配置了API密钥时使用）
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

app = Flask(__name__, template_folder='templates')
CORS(app)

# 配置 - 使用绝对路径确保在Render上也能正常工作
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# 确保上传目录存在
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    print(f"Upload folder created at: {UPLOAD_FOLDER}")
except Exception as e:
    print(f"Error creating upload folder: {e}")

# 存储上传的文件数据
uploaded_files = {}

@app.route('/')
def index():
    """返回前端页面"""
    return render_template('index.html')

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_excel_data(df):
    """分析Excel数据并生成数据摘要"""
    analysis = {
        'row_count': len(df),
        'column_count': len(df.columns),
        'columns': list(df.columns),
        'data_types': {col: str(dtype) for col, dtype in df.dtypes.items()},
        'sample_data': df.head(5).to_dict('records'),
        'null_counts': df.isnull().sum().to_dict(),
        'numeric_columns': list(df.select_dtypes(include=['number']).columns),
        'text_columns': list(df.select_dtypes(include=['object']).columns)
    }
    return analysis

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """上传Excel文件"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件被上传'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        try:
            file.save(filepath)
            
            # 读取Excel文件
            if filename.endswith('.csv'):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)
            
            # 分析数据
            analysis = analyze_excel_data(df)
            
            # 存储文件信息
            file_id = unique_filename
            uploaded_files[file_id] = {
                'filename': filename,
                'filepath': filepath,
                'dataframe': df,
                'analysis': analysis,
                'uploaded_at': datetime.now().isoformat()
            }
            
            return jsonify({
                'success': True,
                'file_id': file_id,
                'filename': filename,
                'analysis': analysis
            })
            
        except Exception as e:
            return jsonify({'error': f'文件处理失败: {str(e)}'}), 500
    
    return jsonify({'error': '不支持的文件格式'}), 400

@app.route('/api/files', methods=['GET'])
def list_files():
    """获取已上传的文件列表"""
    files_list = []
    for file_id, file_info in uploaded_files.items():
        files_list.append({
            'file_id': file_id,
            'filename': file_info['filename'],
            'uploaded_at': file_info['uploaded_at'],
            'row_count': file_info['analysis']['row_count'],
            'column_count': file_info['analysis']['column_count']
        })
    
    return jsonify({'files': files_list})

@app.route('/api/file/<file_id>/data', methods=['GET'])
def get_file_data(file_id):
    """获取文件数据"""
    if file_id not in uploaded_files:
        return jsonify({'error': '文件不存在'}), 404
    
    file_info = uploaded_files[file_id]
    df = file_info['dataframe']
    
    # 获取分页参数
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    # 分页
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    data = df.iloc[start_idx:end_idx].to_dict('records')
    
    return jsonify({
        'data': data,
        'total': len(df),
        'page': page,
        'per_page': per_page,
        'total_pages': (len(df) + per_page - 1) // per_page
    })

@app.route('/api/file/<file_id>/query', methods=['POST'])
def query_data(file_id):
    """自然语言查询数据"""
    if file_id not in uploaded_files:
        return jsonify({'error': '文件不存在'}), 404
    
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': '问题不能为空'}), 400
    
    file_info = uploaded_files[file_id]
    df = file_info['dataframe']
    analysis = file_info['analysis']
    
    try:
        # 构建数据上下文
        data_context = f"""
        数据集信息：
        - 总行数：{analysis['row_count']}
        - 总列数：{analysis['column_count']}
        - 列名：{', '.join(analysis['columns'])}
        - 数据类型：{json.dumps(analysis['data_types'], ensure_ascii=False)}
        - 数值列：{', '.join(analysis['numeric_columns'])}
        - 文本列：{', '.join(analysis['text_columns'])}
        
        示例数据：
        {json.dumps(analysis['sample_data'], ensure_ascii=False, indent=2)}
        """
        
        # 使用OpenAI API进行问答
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or not OPENAI_AVAILABLE:
            # 如果没有API密钥或openai不可用，使用简单的规则匹配
            response_text = simple_query_response(question, df, analysis)
        else:
            client = openai.OpenAI(api_key=api_key)
            
            prompt = f"""
            你是一个数据分析助手。基于以下Excel数据信息回答用户的问题。
            
            {data_context}
            
            用户问题：{question}
            
            请提供准确、简洁的回答。如果需要计算，请给出具体数值。
            如果问题涉及数据筛选或统计，请说明你的分析过程。
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的数据分析助手，擅长分析Excel数据并回答相关问题。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            response_text = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': response_text
        })
        
    except Exception as e:
        return jsonify({'error': f'查询失败: {str(e)}'}), 500

def simple_query_response(question, df, analysis):
    """简单的查询响应（当没有OpenAI API时使用）"""
    question_lower = question.lower()
    
    # 检查是否询问某个列的唯一值（如：产品种类有哪些、有哪些产品等）
    for col in analysis['columns']:
        col_lower = col.lower()
        # 匹配问题中是否包含列名或相关关键词
        if col in question or col_lower in question_lower:
            # 检查是否在询问该列有哪些值
            if any(keyword in question for keyword in ['有哪些', '什么', '种类', '类型', '包含', '都有', '列出', '显示', '所有']):
                unique_values = df[col].dropna().unique()
                if len(unique_values) > 0:
                    if len(unique_values) <= 20:
                        values_str = '、'.join([str(v) for v in unique_values])
                        return f"{col}包含以下{len(unique_values)}个不同的值：\n{values_str}"
                    else:
                        # 如果值太多，只显示前20个
                        values_str = '、'.join([str(v) for v in unique_values[:20]])
                        return f"{col}共有{len(unique_values)}个不同的值，前20个为：\n{values_str}"
    
    # 检查是否询问行数
    if '行' in question or '记录' in question or '总数' in question:
        return f"数据集共有 {analysis['row_count']} 行记录。"
    
    # 检查是否询问列数
    if '列' in question or '字段' in question:
        return f"数据集共有 {analysis['column_count']} 列，分别是：{', '.join(analysis['columns'])}。"
    
    # 检查是否询问列名
    if '列名' in question or '字段名' in question or '有哪些列' in question:
        return f"数据集的列名包括：{', '.join(analysis['columns'])}。"
    
    # 检查是否询问数据类型
    if '类型' in question or '数据类型' in question:
        type_info = '\n'.join([f"- {col}: {dtype}" for col, dtype in analysis['data_types'].items()])
        return f"各列的数据类型：\n{type_info}"
    
    # 检查是否询问空值
    if '空' in question or '缺失' in question or 'null' in question_lower:
        null_info = '\n'.join([f"- {col}: {count} 个空值" for col, count in analysis['null_counts'].items() if count > 0])
        if null_info:
            return f"数据中的空值统计：\n{null_info}"
        else:
            return "数据中没有空值。"
    
    # 检查是否询问数值列的统计信息
    if '统计' in question or '平均' in question or '总和' in question:
        if analysis['numeric_columns']:
            stats_info = []
            for col in analysis['numeric_columns']:
                if pd.api.types.is_numeric_dtype(df[col]):
                    stats_info.append(f"- {col}: 平均值={df[col].mean():.2f}, 总和={df[col].sum():.2f}, 最大值={df[col].max():.2f}, 最小值={df[col].min():.2f}")
            return f"数值列的统计信息：\n" + "\n".join(stats_info)
        else:
            return "数据中没有数值列。"
    
    # 默认响应
    return f"我理解您的问题是：{question}\n\n基于当前数据集（{analysis['row_count']}行 × {analysis['column_count']}列），我可以帮您分析数据内容、统计信息、数据类型等。请尝试更具体的问题，比如：\n- 数据有多少行？\n- 有哪些列？\n- 数值列的统计信息是什么？\n- 哪些列有空值？\n- 某个列有哪些值？（如：产品名称有哪些？）"

@app.route('/api/file/<file_id>/columns', methods=['GET'])
def get_columns(file_id):
    """获取文件的列信息"""
    if file_id not in uploaded_files:
        return jsonify({'error': '文件不存在'}), 404
    
    file_info = uploaded_files[file_id]
    analysis = file_info['analysis']
    
    columns_info = []
    for col in analysis['columns']:
        columns_info.append({
            'name': col,
            'type': analysis['data_types'][col],
            'null_count': analysis['null_counts'][col],
            'is_numeric': col in analysis['numeric_columns']
        })
    
    return jsonify({'columns': columns_info})

@app.route('/api/file/<file_id>/stats', methods=['GET'])
def get_statistics(file_id):
    """获取数据统计信息"""
    if file_id not in uploaded_files:
        return jsonify({'error': '文件不存在'}), 404
    
    file_info = uploaded_files[file_id]
    df = file_info['dataframe']
    analysis = file_info['analysis']
    
    stats = {
        'basic': {
            'row_count': analysis['row_count'],
            'column_count': analysis['column_count'],
            'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"
        },
        'null_counts': analysis['null_counts'],
        'data_types': analysis['data_types']
    }
    
    # 数值列统计
    if analysis['numeric_columns']:
        numeric_stats = {}
        for col in analysis['numeric_columns']:
            if pd.api.types.is_numeric_dtype(df[col]):
                numeric_stats[col] = {
                    'mean': float(df[col].mean()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'sum': float(df[col].sum())
                }
        stats['numeric'] = numeric_stats
    
    return jsonify(stats)

@app.route('/api/file/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    """删除文件"""
    if file_id not in uploaded_files:
        return jsonify({'error': '文件不存在'}), 404
    
    file_info = uploaded_files[file_id]
    
    try:
        # 删除物理文件
        if os.path.exists(file_info['filepath']):
            os.remove(file_info['filepath'])
        
        # 从内存中删除
        del uploaded_files[file_id]
        
        return jsonify({'success': True, 'message': '文件删除成功'})
        
    except Exception as e:
        return jsonify({'error': f'删除失败: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'uploaded_files_count': len(uploaded_files),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # 生产环境配置
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)

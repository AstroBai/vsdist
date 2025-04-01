import sys
import json
import base64
import matplotlib.pyplot as plt
import io

def generate_image(data):
    fig, ax = plt.subplots()
    
    # 绘制文本信息
    ax.text(0.5, 0.7, f'Burn-in rate: {data}', fontsize=15, ha='center', va='center')
    
    
    ax.set_title("Generated Plot")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    
    # 保存图片到内存
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # 编码为 Base64
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    
    return img_base64

if __name__ == "__main__":
    # 读取 VS Code 传递的 JSON 数据
    input_data = sys.stdin.read()
    data = json.loads(input_data)
    # 解析参数
    
    # 生成图片并返回 Base64 编码
    img_data = generate_image(data)
    
    # 通过 stdout 传递结果回 VS Code
    print(json.dumps({"image": img_data}))
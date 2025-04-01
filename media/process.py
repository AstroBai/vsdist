import sys
import json
import base64
import matplotlib.pyplot as plt
import io

def generate_image(burnin):
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, f'Burn-in rate: {burnin}', fontsize=20, ha='center')
    ax.set_title("Generated Plot")
    
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
    
    # 生成图片并返回 Base64 编码
    img_data = generate_image(data['burnin'])
    
    # 通过 stdout 传递结果回 VS Code
    print(json.dumps({"image": img_data}))

import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import * as cp from 'child_process';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('vsdist.start', (uri: vscode.Uri) => {

        const folderPath = uri && fs.statSync(uri.fsPath).isDirectory() ? uri.fsPath : undefined;
        if (!folderPath) {
            vscode.window.showErrorMessage("请在资源管理器中选中一个文件夹。");
            return;
        }

        const panel = vscode.window.createWebviewPanel(
            'vsdist',
            'VSDist',
            vscode.ViewColumn.One,
            { enableScripts: true }
        );

        const webviewPath = path.join(context.extensionPath, 'media', 'webview.html');
        let htmlContent = fs.readFileSync(webviewPath, 'utf8');

        const scriptUri = panel.webview.asWebviewUri(vscode.Uri.file(
            path.join(context.extensionPath, 'media', 'webview.js')
        ));

        htmlContent = htmlContent.replace('{{scriptUri}}', scriptUri.toString());
        panel.webview.html = htmlContent;

        panel.webview.onDidReceiveMessage(
            (message) => {
                if (message.command === 'submit') {

                    const burnin = message.data.burnin;
					const parameters = message.data.parameters;
					const color = message.data.color;

                    // 运行 Python 处理数据
                    const pythonPath = path.join(context.extensionPath, 'media', 'process.py');
                    const process = cp.spawn('python3', [pythonPath]);

                    process.stdin.write(JSON.stringify({ folderPath, burnin, parameters, color }));
                    process.stdin.end();

                    let outputData = '';
                    process.stdout.on('data', (data) => {
                        outputData += data.toString();
                    });

                    process.stderr.on('data', (data) => {
                        console.error(`Python 错误: ${data.toString()}`);
                    });

                    process.on('close', (code) => {
                        if (code === 0) {
                            try {
                                const result = JSON.parse(outputData);
                                panel.webview.postMessage({ command: 'displayImage', image: result.image });
                            } catch (err) {
                                vscode.window.showErrorMessage("处理 Python 输出时出错！");
                            }
                        } else {
                            vscode.window.showErrorMessage("Python 运行失败！");
                        }
                    });
                }
            },
            undefined,
            context.subscriptions
        );
    });

    context.subscriptions.push(disposable);
}

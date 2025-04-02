import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import * as cp from 'child_process';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('vsdist.start', (uri: vscode.Uri) => {

        const folderpath = uri && fs.statSync(uri.fsPath).isDirectory() ? uri.fsPath : undefined;
        if (!folderpath) {
            vscode.window.showErrorMessage("Please select a folder.");
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
					const legend = message.data.legend;
					const color = message.data.color;
					const fontsize = message.data.fontsize;
					const linewidth = message.data.linewidth;
					const alpha = message.data.alpha;
					const filled = message.data.filled;

                    vscode.window.showInformationMessage(`Python Process Begins.`);
                    const pythonPath = path.join(context.extensionPath, 'media', 'process.py');
                    const process = cp.spawn('python3', [pythonPath]);

                    process.stdin.write(JSON.stringify({ folderpath, burnin, parameters, color, fontsize, linewidth, alpha, filled, legend }));
                    process.stdin.end();

                    let outputData = '';
                    process.stdout.on('data', (data) => {
                        outputData += data.toString();
                    });

                    process.stderr.on('data', (data) => {
                        console.error(`Python Failed: ${data.toString()}`);
                    });

                    process.on('close', (code) => {
                        if (code === 0) {
                            vscode.window.showInformationMessage(`Python Process Finished.`);
                            try {
                                const result = JSON.parse(outputData);
                                panel.webview.postMessage({ command: 'displayImage', image: result.image });
                            } catch (err) {
                                vscode.window.showWarningMessage(`Some strange things happened but have nothing to do with Python (please report this as a issue): ${err}`);
                            }
                        } else {
                            vscode.window.showErrorMessage("Python Failed to Run.");
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

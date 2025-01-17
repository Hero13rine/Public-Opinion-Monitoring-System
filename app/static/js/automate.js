let isRunning = false;
let statusInterval = null;

// 更新状态信息
function updateStatus(message, type = 'text-muted') {
    const statusDiv = document.getElementById('status');
    statusDiv.className = type;
    statusDiv.textContent = `状态：${message}`;
}

// 检查任务状态
async function checkAnalysisStatus() {
    try {
        const response = await fetch('/automate/status', { method: 'GET' });
        const data = await response.json();
        if (data.status === "running") {
            isRunning = true;
            updateStatus('分析中...', 'text-primary');
            document.getElementById('startAnalysis').disabled = true;
            document.getElementById('stopAnalysis').disabled = false;
        } else {
            isRunning = false;
            updateStatus('分析已停止', 'text-success');
            document.getElementById('startAnalysis').disabled = false;
            document.getElementById('stopAnalysis').disabled = true;
            clearInterval(statusInterval); // 停止轮询
        }
    } catch (error) {
        console.error('检查分析状态失败:', error);
    }
}

// 开始分析
async function startAnalysis() {
    if (isRunning) return;

    isRunning = true;
    document.getElementById('startAnalysis').disabled = true;
    document.getElementById('stopAnalysis').disabled = false;
    updateStatus('分析中...', 'text-primary');

    try {
        const response = await fetch('/automate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'start' })
        });
        const data = await response.json();
        if (data.message === "分析任务已启动") {
            console.log("自动化分析已启动");
            statusInterval = setInterval(checkAnalysisStatus, 5000); // 每 5 秒检查一次状态
        } else {
            console.warn("无法启动分析:", data.message);
            updateStatus('启动分析失败', 'text-danger');
            stopAnalysis();
        }
    } catch (error) {
        console.error('启动分析失败:', error);
        updateStatus('启动分析失败', 'text-danger');
        stopAnalysis();
    }
}

// 停止分析
async function stopAnalysis() {
    if (!isRunning) return;

    isRunning = false;
    document.getElementById('startAnalysis').disabled = false;
    document.getElementById('stopAnalysis').disabled = true;
    updateStatus('正在停止...', 'text-warning');

    try {
        const response = await fetch('/automate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'stop' })
        });
        const data = await response.json();
        console.log(data.message);
        updateStatus('分析已停止', 'text-success');
        clearInterval(statusInterval); // 停止轮询
    } catch (error) {
        console.error('停止分析失败:', error);
        updateStatus('停止分析失败', 'text-danger');
    }
}

// 事件绑定
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('startAnalysis').addEventListener('click', startAnalysis);
    document.getElementById('stopAnalysis').addEventListener('click', stopAnalysis);
    checkAnalysisStatus(); // 页面加载时检查状态
});

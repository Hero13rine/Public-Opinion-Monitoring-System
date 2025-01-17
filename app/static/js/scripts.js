document.getElementById('submit-button').addEventListener('click', () => {
    const weiboText = document.getElementById('weibo-text').value;

    if (!weiboText.trim()) {
        alert('请输入微博内容！');
        return;
    }

    fetch('/evaluate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: weiboText })
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        if (data.error) {
            resultDiv.innerHTML = `<p style="color: red;">错误：${data.error}</p>`;
        } else {
            const sensitiveWords = data.sensitive_words;
            if (sensitiveWords.length > 0) {
                let resultHTML = '<h3>检测结果：</h3><ul>';
                sensitiveWords.forEach(word => {
                    resultHTML += `<li>${word.word}（危险等级：${word.level}）</li>`;
                });
                resultHTML += '</ul>';
                resultDiv.innerHTML = resultHTML;
            } else {
                resultDiv.innerHTML = '<p style="color: green;">未检测到敏感词。</p>';
            }
        }
    })
    .catch(error => {
        alert('请求失败，请稍后再试！');
        console.error(error);
    });
});

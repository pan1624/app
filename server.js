const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const app = express();
const upload = multer({ dest: 'uploads/' });


// 處理上傳的影片檔案
app.post('/upload', upload.single('file'), (req, res) => {
    console.log('收到上傳請求:');
    console.log('Body:', req.body);
    console.log('File:', req.file);

    const pose = req.body.pose; // 動作名稱
    const tempPath = req.file.path; // 上傳檔案的暫存路徑
    const targetPath = path.join(__dirname, 'videos', req.file.originalname); // 最終儲存路徑

    // 確保目標目錄存在
    if (!fs.existsSync(path.dirname(targetPath))) {
        fs.mkdirSync(path.dirname(targetPath), { recursive: true });
    }

    // 移動檔案到 videos 資料夾
    fs.rename(tempPath, targetPath, (err) => {
        if (err) {
            console.error('檔案儲存失敗:', err);
            return res.status(500).json({ error: '檔案儲存失敗' });
        }

        console.log('檔案已儲存:', targetPath);

        // 對應的參考影片
        const referenceFilePath = path.join(__dirname, 'app', `${pose}.mp4`);
        console.log('Reference File Path:', referenceFilePath);

        if (!fs.existsSync(referenceFilePath)) {
            console.error('參考影片不存在');
            return res.status(400).json({ error: 'Reference video not found' });
        }

        // 模擬相似度計算（基於文件大小）
        console.log('開始計算相似度...');

        const pythonProcess = spawn('python', ['app.py', targetPath, referenceFilePath]);

        let output = '';

        pythonProcess.stdout.on('data', (data) => {
            console.log('Python 輸出:', data.toString());
            output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error('Python 錯誤:', data.toString());
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                console.error(`Python 腳本退出，代碼: ${code}`);
                return res.status(500).json({ error: '相似度分析失敗' });
            }

            // 確保輸出是有效的 JSON 格式或適合處理的數據
            const similarity = parseFloat(output.trim());
            if (isNaN(similarity)) {
                return res.status(500).json({ error: '無效的相似度值' });
            }

            console.log(`相似度分數: ${similarity}%`);
            res.status(200).json({ similarity });
        });    
    });
});

// 啟動伺服器
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`伺服器運行中，請訪問 http://localhost:${PORT}`);
});

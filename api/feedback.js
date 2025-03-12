export default async function handler(req, res) {
    if (req.method !== 'POST') {
      return res.status(405).json({ error: '仅支持 POST 请求' });
    }
  
    try {
      const { name, email, message, contactMe } = req.body;
  
      console.log('收到反馈:', { name, email, message, contactMe });
  
      return res.status(200).json({ success: true, message: '反馈已收到' });
    } catch (error) {
      console.error('处理反馈时出错:', error);
      return res.status(500).json({ error: '服务器内部错误' });
    }
  }
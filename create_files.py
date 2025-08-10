#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 云函数代码
cloud_code = '''// cloud.js - 云函数定义文件
const AV = require('leancloud-storage');
const nodemailer = require('nodemailer');

// 初始化LeanCloud
AV.init({
  appId: process.env.LEANCLOUD_APP_ID,
  appKey: process.env.LEANCLOUD_APP_KEY,
  masterKey: process.env.LEANCLOUD_APP_MASTER_KEY
});

// 邮件验证云函数
AV.Cloud.define('sendVerificationEmail', async function(request) {
  const { email, token } = request.params;
  
  // 配置邮件服务
  const transporter = nodemailer.createTransporter({
    host: 'smtp.qq.com',
    port: 587,
    secure: false,
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS
    }
  });
  
  // 构建验证链接
  const verificationUrl = `https://your-domain.com/verify.html?token=${token}`;
  
  // 邮件内容
  const mailOptions = {
    from: process.env.SMTP_USER,
    to: email,
    subject: '邮箱验证 - NeverSayNo',
    html: `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .container { max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
          .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
          .button { display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; margin: 20px 0; }
          .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>邮箱验证</h1>
            <p>NeverSayNo 应用</p>
          </div>
          <div class="content">
            <h2>您好！</h2>
            <p>感谢您使用 NeverSayNo 应用。为了确保您的账户安全，请点击下面的按钮验证您的邮箱地址：</p>
            
            <div style="text-align: center;">
              <a href="${verificationUrl}" class="button">验证邮箱地址</a>
            </div>
            
            <p>或者，您也可以复制以下链接到浏览器中打开：</p>
            <p style="word-break: break-all; background: #eee; padding: 10px; border-radius: 5px; font-family: monospace;">
              ${verificationUrl}
            </p>
            
            <p><strong>重要提示：</strong></p>
            <ul>
              <li>此验证链接将在1小时后过期</li>
              <li>如果您没有注册 NeverSayNo 账户，请忽略此邮件</li>
              <li>为了您的账户安全，请不要将此链接分享给他人</li>
            </ul>
          </div>
          <div class="footer">
            <p>此邮件由 NeverSayNo 系统自动发送，请勿回复</p>
            <p>如果您有任何问题，请联系我们的客服团队</p>
          </div>
        </div>
      </body>
      </html>
    `
  };
  
  try {
    await transporter.sendMail(mailOptions);
    console.log(`✅ 验证邮件已发送到: ${email}`);
    return { success: true, message: '邮件发送成功' };
  } catch (error) {
    console.error(`❌ 邮件发送失败: ${error.message}`);
    throw new AV.Cloud.Error('邮件发送失败：' + error.message);
  }
});

// 检查邮箱验证状态云函数
AV.Cloud.define('checkEmailVerificationStatus', async function(request) {
  const { email } = request.params;
  
  try {
    // 查询该邮箱是否有已验证的记录
    const query = new AV.Query('EmailVerification');
    query.equalTo('email', email);
    query.equalTo('isUsed', true);
    
    const results = await query.find();
    
    if (results.length > 0) {
      return { success: true, verified: true };
    } else {
      return { success: true, verified: false };
    }
  } catch (error) {
    console.error(`❌ 检查验证状态失败: ${error.message}`);
    throw new AV.Cloud.Error('检查验证状态失败：' + error.message);
  }
});
'''

# 写入cloud.js文件
with open('cloud.js', 'w', encoding='utf-8') as f:
    f.write(cloud_code)

print('✅ cloud.js 文件已创建成功！')

# 创建.gitignore文件
gitignore_content = '''node_modules/
.env
*.log
'''

with open('.gitignore', 'w', encoding='utf-8') as f:
    f.write(gitignore_content)

print('✅ .gitignore 文件已创建成功！')

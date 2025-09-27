from flask import Flask, render_template_string

app = Flask(__name__)

# WAF haqqında məlumat səhifəsi
WAF_PAGE = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WAF - Web Application Firewall</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            text-align: center;
            padding: 40px 20px;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header p {
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }
        .content {
            padding: 40px;
        }
        .section {
            margin-bottom: 30px;
            padding: 25px;
            border-radius: 10px;
            background: #f8f9fa;
            border-left: 5px solid #3498db;
        }
        .section h2 {
            color: #2c3e50;
            margin-top: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .section h3 {
            color: #34495e;
            margin: 20px 0 10px 0;
        }
        .highlight {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #2196f3;
            margin: 15px 0;
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .feature-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-top: 3px solid #e74c3c;
        }
        .icon {
            font-size: 1.5em;
            margin-right: 5px;
        }
        ul {
            padding-left: 20px;
        }
        li {
            margin: 8px 0;
        }
        .footer {
            background: #34495e;
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: 40px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> WAF - Web Application Firewall</h1>
            <p>Veb Tətbiqi Firewall Haqqında Ətraflı Məlumat</p>
        </div>

        <div class="content">
            <div class="section">
                <h2><span class="icon"></span>WAF Nədir?</h2>
                <p><strong>Web Application Firewall (WAF)</strong> veb tətbiqlərini müxtəlif kibertəhlükələrdən qorumaq üçün istifadə olunan təhlükəsizlik həllidir.</p>
                
                <div class="highlight">
                    WAF veb tətbiqi və istifadəçi arasında bir qoruyucu qat yaradır və zərərli HTTP/HTTPS sorğularını filtrləyir.
                </div>
            </div>

            <div class="section">
                <h2><span class="icon"></span>WAF-ın Əsas Funksiyaları</h2>
                <div class="feature-grid">
                    <div class="feature-card">
                        <h3> Hücum Qarşısının Alınması</h3>
                        <p>SQL Injection, XSS, CSRF və digər veb hücumlarına qarşı müdafiə</p>
                    </div>
                    <div class="feature-card">
                        <h3> Trafik Monitorinqi</h3>
                        <p>Daxil olan bütün HTTP sorğularının analizi və izlənməsi</p>
                    </div>
                    <div class="feature-card">
                        <h3>Real-vaxt Müdafiəsi</h3>
                        <p>Şübhəli fəaliyyətlərin dərhal aşkarlanması və bloklanması</p>
                    </div>
                    <div class="feature-card">
                        <h3> Hesabat və Analiz</h3>
                        <p>Təhlükəsizlik hadisələri haqqında ətraflı hesabatlar</p>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2><span class="icon"></span>WAF Qoruma Növləri</h2>
                <h3>Əsas Hücum Növlərinə Qarşı Müdafiə:</h3>
                <ul>
                    <li><strong>SQL Injection:</strong> Databaza sorğularına zərərli kodların əlavə edilməsi</li>
                    <li><strong>Cross-Site Scripting (XSS):</strong> Zərərli JavaScript kodlarının yerinə yetirilməsi</li>
                    <li><strong>Cross-Site Request Forgery (CSRF):</strong> İstifadəçinin razılığı olmadan əməliyyatların həyata keçirilməsi</li>
                    <li><strong>DDoS Hücumları:</strong> Serveri yüklənmiş sorğularla iflic etmək</li>
                    <li><strong>Bot Hücumları:</strong> Avtomatik zərərli bot fəaliyyətləri</li>
                    <li><strong>File Upload Attacks:</strong> Zərərli faylların serverə yüklənməsi</li>
                </ul>
            </div>

            <div class="section">
                <h2><span class="icon"></span>WAF Növləri</h2>
                <div class="feature-grid">
                    <div class="feature-card">
                        <h3> Cloud-based WAF</h3>
                        <p>Bulud xidməti olaraq təqdim olunan, asan idarə edilən həll</p>
                    </div>
                    <div class="feature-card">
                        <h3> On-premises WAF</h3>
                        <p>Şirkətin öz infrastrukturunda quraşdırılan həll</p>
                    </div>
                    <div class="feature-card">
                        <h3> Hybrid WAF</h3>
                        <p>Bulud və yerli həllərin birləşməsi</p>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2><span class="icon"></span>WAF-ın Üstünlükləri</h2>
                <ul>
                    <li>Veb tətbiqlərinin təhlükəsizliyinin artırılması</li>
                    <li>Real-vaxt hücum aşkarlanması və qarşısının alınması</li>
                    <li>Compliance tələblərinə uyğunluq (PCI DSS, GDPR)</li>
                    <li>Təhlükəsizlik hadisələrinin detallı qeydiyyatı</li>
                    <li>Performansın yaxşılaşdırılması (keşləmə)</li>
                    <li>SSL/TLS şifrələmə dəstəyi</li>
                </ul>
            </div>

            <div class="section">
                <h2><span class="icon"></span>Məşhur WAF Həlləri</h2>
                <div class="feature-grid">
                    <div class="feature-card">
                        <h3>AWS WAF</h3>
                        <p>Amazon Web Services tərəfindən təklif olunan bulud həlli</p>
                    </div>
                    <div class="feature-card">
                        <h3>Cloudflare WAF</h3>
                        <p>Qlobal CDN və təhlükəsizlik xidməti</p>
                    </div>
                    <div class="feature-card">
                        <h3>F5 BIG-IP ASM</h3>
                        <p>Enterprise səviyyəli təhlükəsizlik həlli</p>
                    </div>
                    <div class="feature-card">
                        <h3>ModSecurity</h3>
                        <p>Açıq mənbə WAF həlli</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            <p> Flask ilə hazırlanmış sadə tətbiq | Port: 5000</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(WAF_PAGE)

if __name__ == '__main__':
    print(" WAF məlumat tətbiqi başladılır...")
    print(" URL: http://localhost:5000")
    print(" Dayandırmaq üçün Ctrl+C basın")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

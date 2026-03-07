import os
import webbrowser

def generate_html_label(data):
    """
    Creates 3 copies of the Sell-X label on one A4 page.
    """
    # Create the HTML for one single label
    single_label_html = f"""
    <div class="label-container">
        <div class="header">
            <div>
                <div class="brand">Sell-X</div>
                <div class="sub-brand">COMPUTERS & ELECTRONICS</div>
            </div>
            <div class="official">Official Delivery</div>
        </div>
        
        <div class="fragile">FRAGILE - HANDLE WITH CARE</div>
        
        <div class="box">
            <div class="label-title">DELIVER TO:</div>
            <div class="name">{data[0]}</div>
            <div class="address">{data[1]}</div>
            <div class="city">{data[2]}</div>
            <div class="phones">
                <span>📞 {data[3]}</span> &nbsp;&nbsp; <span>📱 {data[4]}</span>
            </div>
        </div>
        
        <div class="footer">
            <div>
                <strong>FROM: SELL-X GALLE</strong><br>
                12, Main Street, Galle. | 0912 230 400 | 0703 250 250
            </div>
            <div style="text-align:right">
                <strong>ORIGIN: GALLE</strong>
            </div>
        </div>
    </div>
    """

    # Combine 3 copies into a single page
    full_html = f"""
    <html>
    <head>
        <style>
         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800;900&display=swap');
            @page {{ size: A4; margin: 10mm; }}
            body {{ font-family: 'Inter', Arial, sans-serif; margin: 0; padding: 0; }}
            
            /* Page container to stack 3 labels */
            .page {{ display: flex; flex-direction: column; gap: 20px; }}

            /* Individual Label Styling */
            .label-container {{ 
                width: 170mm; 
                border: 2px solid #000; 
                padding: 15px; 
                position: relative;
                margin: 0 auto;
                background: white;
            }}

            /* Cut line indicator */
            .label-container:not(:last-child)::after {{
                content: "----------------------------  CUT HERE  ----------------------------";
                position: absolute;
                bottom: -18px;
                left: 0;
                width: 100%;
                text-align: center;
                font-size: 10px;
                color: #aaa;
            }}

            .header {{ display: flex; justify-content: space-between; align-items: start; }}
            .brand {{ color: #e60000; font-size: 28px; font-weight: 900; margin: 0; line-height: 1; }}
            .sub-brand {{ font-size: 9px; font-weight: bold; color: #555; letter-spacing: 1px; }}
            .official {{ border: 1px solid #000; padding: 4px 8px; font-size: 11px; font-weight: bold; }}
            
            .fragile {{ 
                background: #e60000; color: white; text-align: center; padding: 8px; 
                margin: 10px 0; font-weight: bold; border: 2px dashed white; 
                outline: 2px solid #e60000; font-size: 16px;
            }}
            
            .box {{ border: 1px solid #ccc; padding: 12px; border-radius: 10px; background: #fefefe; }}
            .label-title {{ color: gray; font-size: 10px; font-weight: bold; margin-bottom: 3px; }}
            .name {{ font-size: 24px; font-weight: bold; color: #001f3f; }}
            .address {{ font-size: 16px; margin: 5px 0; }}
            .city {{ font-size: 20px; font-weight: 900; text-transform: uppercase; border-bottom: 3px solid black; display: inline-block; margin: 5px 0; }}
            .phones {{ font-size: 16px; font-weight: bold; margin-top: 5px; }}
            
            .footer {{ font-size: 9px; border-top: 1px solid #eee; margin-top: 15px; padding-top: 8px; display: flex; justify-content: space-between; }}
            
            @media print {{
                body {{ -webkit-print-color-adjust: exact; }}
            }}
        </style>
    </head>
    <body>
        <div class="page">
            {single_label_html}
            {single_label_html}
            {single_label_html}
        </div>
    </body>
    </html>
    """
    
    file_path = os.path.abspath("temp_label.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    
    webbrowser.open(f"file://{file_path}")
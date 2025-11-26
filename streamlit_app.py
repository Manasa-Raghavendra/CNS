import streamlit as st
import time
import os
import tempfile
from smtp_backend import send_enhanced_email

# Page configuration
st.set_page_config(
    page_title="SMTP Email Client - CNS Project",
    page_icon="📧",
    layout="wide"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 20px;
        background-color: #d4edda;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        margin: 10px 0;
    }
    .error-box {
        padding: 20px;
        background-color: #f8d7da;
        border-radius: 10px;
        border: 1px solid #f5c6cb;
        margin: 10px 0;
    }
    .info-box {
        padding: 15px;
        background-color: #d1ecf1;
        border-radius: 10px;
        border: 1px solid #bee5eb;
        margin: 10px 0;
    }
    .step-box {
        padding: 10px;
        background-color: #e2e3e5;
        border-radius: 5px;
        margin: 5px 0;
        border-left: 4px solid #6c757d;
    }
    .attachment-box {
        padding: 15px;
        background-color: #fff3cd;
        border-radius: 10px;
        border: 1px solid #ffeaa7;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📧 SMTP Protocol Email Client</div>', unsafe_allow_html=True)

# Sidebar for SMTP Explanation
with st.sidebar:
    st.header("🧠 SMTP Protocol Explained")
    st.markdown("""
    **SMTP = Simple Mail Transfer Protocol**
    
    **How it works:**
    """)
    
    steps = [
        "🔌 **Connect** to SMTP server",
        "🔒 **Encrypt** with TLS", 
        "🔐 **Authenticate** with credentials",
        "📝 **Compose** email message",
        "📎 **Attach** files (MIME encoding)",
        "🚀 **Send** via SMTP protocol",
        "✅ **Confirm** delivery"
    ]
    
    for step in steps:
        st.markdown(f'<div class="step-box">{step}</div>', unsafe_allow_html=True)
    
    st.markdown("""
    **Networking Concepts:**
    - Client-Server Architecture
    - TCP Port 587
    - TLS Encryption
    - MIME Protocol for attachments
    - Protocol Communication
    - Authentication
    """)

# Main app - Two columns layout
col1, col2 = st.columns([2, 1])

with col1:
    st.header("✉️ Compose Email")
    
    # Email configuration
    with st.expander("🔧 SMTP Configuration", expanded=True):
        smtp_server = st.selectbox(
            "SMTP Server",
            ["smtp.gmail.com", "smtp.outlook.com", "smtp.mail.yahoo.com", "Custom"],
            key="smtp_server"
        )
        if smtp_server == "Custom":
            smtp_server = st.text_input("Custom SMTP Server", key="custom_smtp")
        
        port = st.number_input("Port", min_value=1, max_value=9999, value=587, key="port")
    
    # Login credentials
    with st.expander("🔐 Login Credentials", expanded=True):
        col_a, col_b = st.columns(2)
        with col_a:
            sender_email = st.text_input("Your Email", placeholder="your.email@gmail.com", key="sender_email")
        with col_b:
            app_password = st.text_input("App Password", type="password", placeholder="16-character app password", key="app_password")
    
    # Email composition
    with st.expander("📝 Email Content", expanded=True):
        receiver_email = st.text_input("To", placeholder="recipient@example.com", key="receiver_email")
        subject = st.text_input("Subject", placeholder="Hello from SMTP Project!", key="subject")
        
        message_type = st.radio("Message Type", ["Plain Text", "HTML"], key="message_type")
        
        if message_type == "Plain Text":
            body = st.text_area("Message Body", height=150, 
                              placeholder="Type your message here...\n\nThis email was sent using SMTP protocol!",
                              key="plain_body")
        else:
            body = st.text_area("HTML Message", height=150, 
                              value="<h2>Hello from SMTP Project!</h2><p>This is an <b>HTML email</b> sent via Python SMTP protocol.</p><p>Demonstrating computer networks concepts!</p>",
                              key="html_body")
    
    # File attachment
    with st.expander("📎 File Attachment", expanded=True):
        st.info("💡 You can attach files like PDF, images, documents, etc.")
        uploaded_file = st.file_uploader(
            "Choose a file to attach", 
            type=['pdf', 'txt', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'zip'],
            help="Maximum file size: 20MB"
        )
        
        if uploaded_file is not None:
            # Display file information
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size / (1024*1024):.2f} MB",
                "File type": uploaded_file.type
            }
            
            st.markdown(f"""
            <div class="attachment-box">
                <h4>📎 File Ready to Attach:</h4>
                <p><strong>Name:</strong> {file_details['Filename']}</p>
                <p><strong>Size:</strong> {file_details['File size']}</p>
                <p><strong>Type:</strong> {file_details['File type']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                attachment_path = tmp_file.name
        else:
            attachment_path = None

    # Send button
    send_button = st.button("🚀 Send Email via SMTP", use_container_width=True, type="primary")
    
    if send_button:
        if not all([sender_email, app_password, receiver_email, subject, body]):
            st.error("❌ Please fill all required fields!")
        else:
            # Show progress animation
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            steps = [
                "🔌 Connecting to SMTP server...",
                "🔒 Starting TLS encryption...", 
                "🔐 Authenticating with server...",
                "📝 Preparing email content...",
                "📎 Processing attachment..." if attachment_path else "📤 Preparing to send...",
                "📤 Sending email via SMTP..."
            ]
            
            for i, step in enumerate(steps):
                status_text.text(step)
                progress_bar.progress((i + 1) * (100 // len(steps)))
                time.sleep(0.5)
            
            # Send the email
            success, message, details = send_enhanced_email(
                sender_email, app_password, receiver_email, subject, body, attachment_path, smtp_server, port
            )
            
            # Clean up temporary file
            if attachment_path and os.path.exists(attachment_path):
                os.unlink(attachment_path)
            
            progress_bar.progress(100)
            
            if success:
                st.balloons()
                
                # Build success message
                success_html = f"""
                <div class="success-box">
                    <h3>✅ {message}</h3>
                    <p><strong>From:</strong> {details['from']}</p>
                    <p><strong>To:</strong> {details['to']}</p>
                    <p><strong>Subject:</strong> {details['subject']}</p>
                    <p><strong>Body Length:</strong> {details['body_length']} characters</p>
                    <p><strong>SMTP Server:</strong> {details['smtp_server']}:{details['port']}</p>
                    <p><strong>HTML Version:</strong> {'Yes' if details['html_included'] else 'No'}</p>
                """
                
                if details['attachment']:
                    attachment = details['attachment']
                    success_html += f"""
                    <p><strong>Attachment:</strong> {attachment['filename']} ({attachment['size_mb']} MB)</p>
                    """
                
                success_html += "</div>"
                
                st.markdown(success_html, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="error-box">
                    <h3>{message}</h3>
                </div>
                """, unsafe_allow_html=True)

with col2:
    st.header("📊 SMTP Process")
    
    st.markdown("""
    <div class="info-box">
    <h4>🔄 Real-time SMTP Flow</h4>
    <p>When you click send:</p>
    <ol>
        <li>Python connects to SMTP server</li>
        <li>Starts secure TLS session</li>
        <li>Authenticates your identity</li>
        <li>Encodes attachment (MIME)</li>
        <li>Transfers email data + file</li>
        <li>Confirms delivery</li>
        <li>Closes connection</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # SMTP Information
    st.markdown("""
    <div class="info-box">
    <h4>📚 Technical Details</h4>
    <p><strong>Protocol:</strong> SMTP (Simple Mail Transfer Protocol)</p>
    <p><strong>Port 587:</strong> Email submission with STARTTLS</p>
    <p><strong>Encryption:</strong> TLS 1.2/1.3</p>
    <p><strong>Authentication:</strong> SMTP AUTH</p>
    <p><strong>MIME:</strong> Multipart email + attachments</p>
    <p><strong>File Support:</strong> PDF, Images, Documents, ZIP</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Educational content
    st.markdown("""
    <div class="info-box">
    <h4>🎓 CNS Project Concepts</h4>
    <p>✅ Network Protocols (SMTP)</p>
    <p>✅ MIME Encoding</p>
    <p>✅ File Transfer over Email</p>
    <p>✅ Client-Server Model</p>
    <p>✅ TCP/IP Communication</p>
    <p>✅ Encryption & Security</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("**Computer Networks Mini-Project | SMTP Protocol with File Attachments** | Built with Streamlit 🎈")
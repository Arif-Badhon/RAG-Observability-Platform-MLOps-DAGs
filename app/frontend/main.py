import streamlit as st
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

st.title("RAG Observability Platform 🚀")
st.sidebar.header("Configuration")

model_type = st.sidebar.selectbox("Model Provider", ["Local (MLX)", "Cloud (HF)"])

if st.button("Check Environment"):
    import platform
    st.write(f"OS: {platform.system()} {platform.release()}")
    st.write(f"Python: {sys.version}")
    
    try:
        import mlx.core
        st.success("✅ MLX is installed and ready for M4 GPU!")
    except ImportError:
        st.warning("⚠️ MLX not found (Expected if running in Docker/Cloud).")

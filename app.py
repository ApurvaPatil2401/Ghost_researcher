import streamlit as st
from agent import ResearchCrew

st.set_page_config(page_title="🛡️ GhostResearcher Pro", layout="wide")

# Custom CSS to make it look "Premium"
st.markdown("""
    <style>
    .stStatus { background-color: #f0f2f6; border-radius: 10px; padding: 10px; }
    .agent-thought { font-family: 'Courier New', Courier, monospace; color: #2e7d32; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ GhostResearcher: Multi-Agent Intelligence")
st.subheader("High-speed industry analysis powered by Groq & CrewAI")

topic = st.text_input("Enter a niche (e.g., 'Self-healing AI in DevOps 2026')", "AI Agents in Finance")

if st.button("Launch Agent Crew"):
    # 1. Create a placeholder for the live logs
    with st.status("🤖 Agents are collaborating...", expanded=True) as status:
        st.write("Initializing Researcher and Analyst agents...")
        
        # 2. Run the Crew
        crew_instance = ResearchCrew()
        # Note: We use kickoff() which returns a CrewOutput object
        result = crew_instance.run(topic)
        
        status.update(label="✅ Research Complete!", state="complete", expanded=False)

    # 3. Display Final Output in a professional layout
    st.divider()
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Final Industry Report")
        st.markdown(result.raw) # CrewAI 2026 output has a .raw attribute
    
    with col2:
        st.markdown("### 📊 Metadata")
        st.info(f"**Model:** Llama-3.3-70b\n\n**Speed:** Ultra-fast (Groq LPU)")
        
        # Add the Download Button we discussed
        st.download_button(
            label="📄 Download Full Report",
            data=result.raw,
            file_name=f"research_{topic}.md",
            mime="text/markdown"
        )
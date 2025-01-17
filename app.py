import streamlit as st
import arxiv
import re
from datetime import datetime
from deep_translator import GoogleTranslator

# Streamlit başlık
if "menu_option" not in st.session_state or st.session_state.menu_option == "Ana Sayfa":
    st.title("arXiv'de Güncel Makine Öğrenmesi Makaleleri")

# Menü butonları
def main_menu():
    st.sidebar.markdown("### Menü")
    
    # Menü butonları
    if st.sidebar.button("Ana Sayfa"):
        st.session_state.menu_option = "Ana Sayfa"
    if st.sidebar.button("Makine Öğrenmesi"):
        st.session_state.menu_option = "Makine Öğrenmesi"
    if st.sidebar.button("Transformers"):
        st.session_state.menu_option = "Transformers"

    # Sosyal medya bağlantıları (sadece Ana Sayfa'da göster)
    if st.session_state.menu_option == "Ana Sayfa":
        st.sidebar.markdown("""
        <div style="text-align: center;">
            <a href="https://github.com/emredeveloper" target="_blank" style="margin-right: 10px;">
                <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="30" alt="GitHub">
            </a>
            <a href="https://www.linkedin.com/in/cihatemrekaratas/" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="30" alt="LinkedIn">
            </a>
        </div>
        """, unsafe_allow_html=True)

# Session state'te menü seçeneğini saklama
if "menu_option" not in st.session_state:
    st.session_state.menu_option = "Ana Sayfa"

# Menüyü yükle
main_menu()

# Ana Sayfa içeriği
if st.session_state.menu_option == "Ana Sayfa":
    # Kullanıcıdan alınacak parametreler
    max_results = st.sidebar.number_input("Gösterilecek Makale Sayısı", min_value=1, max_value=100, value=10)
    sort_by = st.sidebar.selectbox("Sıralama Kriteri", ["Yeniden Eskiye", "Eskiden Yeniye"])

    # ArXiv'den makaleleri çekme
    @st.cache_data
    def fetch_articles(max_results, sort_by):
        query = "cat:cs.LG"
        sort_order = arxiv.SortOrder.Descending if sort_by == "Yeniden Eskiye" else arxiv.SortOrder.Ascending

        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=sort_order
        )
        return list(client.results(search))

    articles = fetch_articles(max_results, sort_by)

    # Regex: GitHub linklerini bulma
    github_pattern = r"https://github\.com/[a-zA-Z0-9\-_]+/[a-zA-Z0-9\-_]+"

    # Session state: Like ve kullanıcı etkileşimlerini saklama
    if "likes" not in st.session_state:
        st.session_state.likes = {}
    if "user_likes" not in st.session_state:
        st.session_state.user_likes = set()

    # Çeviri fonksiyonu
    def translate_text(text, dest_language="tr"):
        try:
            translated = GoogleTranslator(source='auto', target=dest_language).translate(text)
            return translated
        except Exception as e:
            st.error(f"Çeviri hatası: {e}")
            return text

    # CSS ile modern stil
    def load_custom_css():
        st.markdown(
            """
            <style>
            .card {
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin-bottom: 10px;
                background-color: #fff;
                border: 1px solid #ccc;
            }
            .card:hover {
                background-color: #f0f0f0;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .stButton button {
                background-color: #2b3e50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 11px;
            }
            .stButton button:hover {
                background-color: #1a252f;
            }
            h1, h2, h3, h4, h5, h6 {
                color: #2c3e50;
                font-size: 18px;
            }
            .sidebar .block-container {
                padding: 20px;
                background-color: #f8f9fa;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    load_custom_css()

    # Makale bilgilerini görüntüleme
    st.write(f"**{max_results}** adet makale gösteriliyor:")
    for i, result in enumerate(articles):
        with st.container():
            
            st.markdown(f"<h2>arXiv'de Güncel Makine Öğrenmesi Makaleleri</h3>", unsafe_allow_html=True)
            st.markdown('<div class="card">', unsafe_allow_html=True)

            # Başlık
            title = result.title
            if st.button(f"Başlığı Çevir ({i})", key=f"translate_title_{i}"):
                title = translate_text(title)
            st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)

            # Yazarlar
            st.markdown(f"<h5>Yazarlar: {', '.join(author.name for author in result.authors)}</h5>", unsafe_allow_html=True)

            # Yayın tarihi
            published_date = result.published.strftime("%Y-%m-%d %H:%M")
            st.markdown(f"<h5>Yayın Tarihi: {published_date}</h5>", unsafe_allow_html=True)

            # Özet
            summary = result.summary
            if st.button(f"Özeti Çevir ({i})", key=f"translate_summary_{i}"):
                summary = translate_text(summary)
            with st.expander("Özeti Görüntüle"):
                st.write(summary)

            # GitHub linkleri
            github_links = re.findall(github_pattern, result.summary)
            if github_links:
                st.markdown("**GitHub Repository:**")
                for link in github_links:
                    st.markdown(f"- [{link}]({link})")
            else:
                st.markdown("**GitHub Repository:** Bulunamadı.")

            # Makale linki
            st.markdown(f"**Makale Linki:** [arXiv]({result.entry_id})")

            # Like butonu
            if i not in st.session_state.likes:
                st.session_state.likes[i] = 0

            if i in st.session_state.user_likes:
                st.button(f"❤️ Beğendiniz ({st.session_state.likes[i]})", key=f"liked_{i}", disabled=True)
            else:
                if st.button(f"👍 Beğen ({st.session_state.likes[i]})", key=f"like_{i}"):
                    st.session_state.likes[i] += 1
                    st.session_state.user_likes.add(i)

            st.markdown('</div>', unsafe_allow_html=True)

# Makine Öğrenmesi sayfası
elif st.session_state.menu_option == "Makine Öğrenmesi":
    st.write("## Makine Öğrenmesi")
    st.write("Makine öğrenmesi genel konuları burada yer alacak.")

# Transformers sayfası
elif st.session_state.menu_option == "Transformers":
    st.write("## Transformers")
    st.write("Transformers yapıları hakkında bilgiler burada yer alacak.")
import re
from datetime import datetime, timedelta

import arxiv
import streamlit as st
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="arXiv'de Güncel Makine Öğrenmesi Makaleleri",
    page_icon="📚",
    layout="wide",
)

# Regex pattern for GitHub links (defined globally)
github_pattern = r"https://github\.com/[a-zA-Z0-9\-_]+/[a-zA-Z0-9\-_]+"

MENU_OPTIONS = ["Ana Sayfa", "Makine Öğrenmesi", "Transformers", "Favoriler"]


def render_social_links() -> None:
    st.sidebar.markdown(
        """
        <div style="text-align: center;">
            <a href="https://github.com/emredeveloper" target="_blank" style="margin-right: 10px;">
                <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="30" alt="GitHub">
            </a>
            <a href="https://www.linkedin.com/in/cihatemrekaratas/" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="30" alt="LinkedIn">
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main_menu() -> None:
    st.sidebar.markdown("### Menü")

    if "menu_option" not in st.session_state:
        st.session_state.menu_option = MENU_OPTIONS[0]

    selected_option = st.sidebar.radio(
        "Sayfa seçiniz",
        MENU_OPTIONS,
        index=MENU_OPTIONS.index(st.session_state.menu_option),
        label_visibility="collapsed",
    )
    st.session_state.menu_option = selected_option

    if selected_option == "Ana Sayfa":
        render_social_links()


st.title("📚 arXiv'de Güncel Makine Öğrenmesi Makaleleri")

# Favoriler ve makaleler için session state
if "favorites" not in st.session_state:
    st.session_state.favorites = set()
if "articles" not in st.session_state:
    st.session_state.articles = []
if "likes" not in st.session_state:
    st.session_state.likes = {}
if "user_likes" not in st.session_state:
    st.session_state.user_likes = set()


@st.cache_resource(show_spinner=False)
def get_translator(dest_language: str) -> GoogleTranslator:
    return GoogleTranslator(source="auto", target=dest_language)


@st.cache_data(ttl=600, show_spinner=False)
def fetch_articles(max_results: int, sort_by: str):
    query = "cat:cs.LG"
    sort_order = (
        arxiv.SortOrder.Descending
        if sort_by == "Yeniden Eskiye"
        else arxiv.SortOrder.Ascending
    )

    client = arxiv.Client(
        page_size=min(max_results, 100),
        delay=3,
        num_retries=2,
    )

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=sort_order,
    )
    return list(client.results(search))


def translate_text(text: str, dest_language: str = "tr") -> str:
    try:
        translator = get_translator(dest_language)
        return translator.translate(text)
    except Exception as exc:
        st.error(f"Çeviri hatası: {exc}")
        return text


def load_custom_css() -> None:
    st.markdown(
        """
        <style>
        .card {
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        .card h3 {
            color: #2c3e50;
            font-size: 20px;
            margin-top: 0;
            margin-bottom: 10px;
        }
        .card h5 {
            color: #34495e;
            font-size: 16px;
            margin-bottom: 5px;
        }
        .stButton button {
            background-color: #3498db;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #2980b9;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Menüyü yükle
main_menu()

# Ana Sayfa içeriği
if st.session_state.menu_option == "Ana Sayfa":
    # Kullanıcıdan alınacak parametreler
    max_results = st.sidebar.number_input("Gösterilecek Makale Sayısı", min_value=1, max_value=100, value=10)
    sort_by = st.sidebar.selectbox("Sıralama Kriteri", ["Yeniden Eskiye", "Eskiden Yeniye"])

    # Tarih aralığı filtresi
    start_date = st.sidebar.date_input("Başlangıç Tarihi", datetime.now() - timedelta(days=30))
    end_date = st.sidebar.date_input("Bitiş Tarihi", datetime.now())

    # ArXiv'den makaleleri çekme
    articles = fetch_articles(max_results, sort_by)

    # Tarih aralığına göre filtreleme
    articles = [article for article in articles if start_date <= article.published.date() <= end_date]

    # Store articles in session state
    st.session_state.articles = articles
    valid_indices = set(range(len(articles)))
    st.session_state.likes = {
        idx: st.session_state.likes.get(idx, 0) for idx in valid_indices
    }
    st.session_state.user_likes = {
        idx for idx in st.session_state.user_likes if idx in valid_indices
    }
    st.session_state.favorites = {
        idx for idx in st.session_state.favorites if idx in valid_indices
    }

    if not articles:
        st.warning("Belirtilen tarih aralığında makale bulunamadı.")
    else:
        load_custom_css()

        # Makale bilgilerini görüntüleme
        st.write(f"**{max_results}** adet makale gösteriliyor:")
        for i, result in enumerate(articles):
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)

                # Başlık
                title = result.title
                if st.button(f"📄 Başlığı Çevir ({i})", key=f"translate_title_{i}"):
                    title = translate_text(title)
                st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)

                # Yazarlar
                st.markdown(f"<h5>👤 Yazarlar: {', '.join(author.name for author in result.authors)}</h5>", unsafe_allow_html=True)

                # Yayın tarihi
                published_date = result.published.strftime("%Y-%m-%d %H:%M")
                st.markdown(f"<h5>📅 Yayın Tarihi: {published_date}</h5>", unsafe_allow_html=True)

                # Özet
                summary = result.summary
                if st.button(f"📝 Özeti Çevir ({i})", key=f"translate_summary_{i}"):
                    summary = translate_text(summary)
                with st.expander("📖 Özeti Görüntüle"):
                    st.write(summary)

                # GitHub linkleri
                github_links = re.findall(github_pattern, result.summary)
                if github_links:
                    st.markdown("**💻 GitHub Repository:**")
                    for link in github_links:
                        st.markdown(f"- [{link}]({link})")
                else:
                    st.markdown("**💻 GitHub Repository:** Bulunamadı.")

                # Makale linki
                st.markdown(f"**🔗 Makale Linki:** [arXiv]({result.entry_id})")

                # Like butonu
                if i not in st.session_state.likes:
                    st.session_state.likes[i] = 0

                if i in st.session_state.user_likes:
                    st.button(f"❤️ Beğendiniz ({st.session_state.likes[i]})", key=f"liked_{i}", disabled=True)
                else:
                    if st.button(f"👍 Beğen ({st.session_state.likes[i]})", key=f"like_{i}"):
                        st.session_state.likes[i] += 1
                        st.session_state.user_likes.add(i)

                # Favorilere ekle butonu
                if st.button(f"⭐ Favorilere Ekle ({i})", key=f"favorite_{i}"):
                    st.session_state.favorites.add(i)
                    st.success("Makale favorilere eklendi! 🎉")

                st.markdown('</div>', unsafe_allow_html=True)

# Favoriler sayfası
elif st.session_state.menu_option == "Favoriler":
    st.write("## ⭐ Favoriler")
    if not st.session_state.favorites:
        st.write("Henüz favori makaleniz yok.")
    else:
        for i in sorted(st.session_state.favorites):
            if i < len(st.session_state.articles):  # Ensure the index is valid
                result = st.session_state.articles[i]
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)

                    # Başlık
                    st.markdown(f"<h3>{result.title}</h3>", unsafe_allow_html=True)

                    # Yazarlar
                    st.markdown(f"<h5>👤 Yazarlar: {', '.join(author.name for author in result.authors)}</h5>", unsafe_allow_html=True)

                    # Yayın tarihi
                    published_date = result.published.strftime("%Y-%m-%d %H:%M")
                    st.markdown(f"<h5>📅 Yayın Tarihi: {published_date}</h5>", unsafe_allow_html=True)

                    # Özet
                    with st.expander("📖 Özeti Görüntüle"):
                        st.write(result.summary)

                    # GitHub linkleri
                    github_links = re.findall(github_pattern, result.summary)
                    if github_links:
                        st.markdown("**💻 GitHub Repository:**")
                        for link in github_links:
                            st.markdown(f"- [{link}]({link})")
                    else:
                        st.markdown("**💻 GitHub Repository:** Bulunamadı.")

                    # Makale linki
                    st.markdown(f"**🔗 Makale Linki:** [arXiv]({result.entry_id})")

                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning(f"Makale {i} bulunamadı. Lütfen ana sayfadan makaleleri yeniden yükleyin.")

# Makine Öğrenmesi sayfası
elif st.session_state.menu_option == "Makine Öğrenmesi":
    st.write("## 🤖 Makine Öğrenmesi")
    st.write("Makine öğrenmesi genel konuları burada yer alacak.")

# Transformers sayfası
elif st.session_state.menu_option == "Transformers":
    st.write("## ⚡ Transformers")
    st.write("Transformers yapıları hakkında bilgiler burada yer alacak.")

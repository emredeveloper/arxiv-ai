<<<<<<< HEAD
import streamlit as st
from datetime import datetime, timedelta
from database import Database
from utils import (
    extract_github_links, translate_text, format_authors, 
    format_date, get_arxiv_id, load_custom_css, 
    show_success_message, show_error_message, show_info_box,
    validate_date_range
)
from arxiv_client import ArxivClient
=======
import re
from datetime import datetime, timedelta

import arxiv
import streamlit as st
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Latest Machine Learning Papers on arXiv",
    page_icon="📚",
    layout="wide",
)
>>>>>>> 7754dfbb2684360954b29146f332464316a9b4bc

# Page configuration
st.set_page_config(
    page_title="arXiv AI - Makale Takip Sistemi",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database and arXiv client
try:
    db = Database()
    arxiv_client = ArxivClient()
except Exception as e:
    st.error(f"Initialization error: {str(e)}")
    st.stop()

# Load custom CSS
load_custom_css()

# Session state initialization
if "menu_option" not in st.session_state:
    st.session_state.menu_option = "Ana Sayfa"

if "articles" not in st.session_state:
    st.session_state.articles = []

if "user_likes" not in st.session_state:
    st.session_state.user_likes = set()

if "translated_titles" not in st.session_state:
    st.session_state.translated_titles = {}

if "translated_summaries" not in st.session_state:
    st.session_state.translated_summaries = {}

<<<<<<< HEAD

def main_menu():
    """Render the sidebar menu."""
    st.sidebar.markdown("### 📋 Menü")
    
    # Menu buttons
    if st.sidebar.button("🏠 Ana Sayfa", use_container_width=True):
        st.session_state.menu_option = "Ana Sayfa"
        st.rerun()
    
    if st.sidebar.button("🤖 Makine Öğrenmesi", use_container_width=True):
        st.session_state.menu_option = "Makine Öğrenmesi"
        st.rerun()
    
    if st.sidebar.button("⚡ Transformers", use_container_width=True):
        st.session_state.menu_option = "Transformers"
        st.rerun()
    
    if st.sidebar.button("⭐ Favoriler", use_container_width=True):
        st.session_state.menu_option = "Favoriler"
        st.rerun()
    
    if st.sidebar.button("📊 İstatistikler", use_container_width=True):
        st.session_state.menu_option = "İstatistikler"
        st.rerun()
    
    # Social media links (only on homepage)
    if st.session_state.menu_option == "Ana Sayfa":
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🔗 Sosyal Medya")
        st.sidebar.markdown("""
=======
MENU_OPTIONS = ["Home", "Machine Learning", "Transformers", "Favorites"]


def render_social_links() -> None:
    st.sidebar.markdown(
        """
>>>>>>> 7754dfbb2684360954b29146f332464316a9b4bc
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


<<<<<<< HEAD
def render_article_card(article, index=None, show_favorite_button=True):
    """Render an article card with all information and actions."""
    try:
        arxiv_id = get_arxiv_id(article.entry_id)
        
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            # Title with translation
            col1, col2 = st.columns([4, 1])
            with col1:
                title_key = f"title_{arxiv_id}"
                if title_key in st.session_state.translated_titles:
                    title = st.session_state.translated_titles[title_key]
                else:
                    title = article.title
                st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
            
            with col2:
                if st.button("🌐 Çevir", key=f"translate_title_{arxiv_id}_{index}"):
                    with st.spinner("Çevriliyor..."):
                        translated = translate_text(article.title)
                        st.session_state.translated_titles[title_key] = translated
                        db.log_interaction(arxiv_id, "translate_title")
                        st.rerun()
            
            # Authors
            authors_str = format_authors(article.authors)
            st.markdown(f"<h5>👤 Yazarlar: {authors_str}</h5>", unsafe_allow_html=True)
            
            # Published date
            published_date = format_date(article.published)
            st.markdown(f"<h5>📅 Yayın Tarihi: {published_date}</h5>", unsafe_allow_html=True)
            
            # Summary with translation
            summary_key = f"summary_{arxiv_id}"
            with st.expander("📖 Özeti Görüntüle"):
                if summary_key in st.session_state.translated_summaries:
                    summary = st.session_state.translated_summaries[summary_key]
                else:
                    summary = article.summary
                st.write(summary)
                
                if st.button("🌐 Özeti Çevir", key=f"translate_summary_{arxiv_id}_{index}"):
                    with st.spinner("Özet çevriliyor..."):
                        translated = translate_text(article.summary)
                        st.session_state.translated_summaries[summary_key] = translated
                        db.log_interaction(arxiv_id, "translate_summary")
                        st.rerun()
            
            # GitHub links
            github_links = extract_github_links(article.summary)
            if github_links:
                st.markdown("**💻 GitHub Repository:**")
                for link in github_links:
                    st.markdown(f"- [{link}]({link})")
            else:
                st.markdown("**💻 GitHub Repository:** Bulunamadı.")
            
            # Article link
            st.markdown(f"**🔗 Makale Linki:** [arXiv]({article.entry_id})")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Like button
                like_count = db.get_like_count(arxiv_id)
                if arxiv_id in st.session_state.user_likes:
                    st.button(f"❤️ Beğendiniz ({like_count})", 
                             key=f"liked_{arxiv_id}_{index}", disabled=True)
                else:
                    if st.button(f"👍 Beğen ({like_count})", key=f"like_{arxiv_id}_{index}"):
                        new_count = db.add_like(arxiv_id)
                        st.session_state.user_likes.add(arxiv_id)
                        db.log_interaction(arxiv_id, "like")
                        show_success_message(f"Beğendiniz! Toplam: {new_count}")
                        st.rerun()
            
            with col2:
                # Favorite button
                if show_favorite_button:
                    is_fav = db.is_favorite(arxiv_id)
                    if is_fav:
                        if st.button(f"⭐ Favorilerde", key=f"unfavorite_{arxiv_id}_{index}"):
                            db.remove_favorite(arxiv_id)
                            db.log_interaction(arxiv_id, "unfavorite")
                            show_success_message("Favorilerden çıkarıldı!")
                            st.rerun()
                    else:
                        if st.button(f"☆ Favorilere Ekle", key=f"favorite_{arxiv_id}_{index}"):
                            db.add_favorite(
                                arxiv_id=arxiv_id,
                                title=article.title,
                                authors=[author.name for author in article.authors],
                                summary=article.summary,
                                published_date=format_date(article.published),
                                entry_url=article.entry_id,
                                github_links=github_links
                            )
                            db.log_interaction(arxiv_id, "favorite")
                            show_success_message("Favorilere eklendi! 🎉")
                            st.rerun()
            
            with col3:
                # PDF download link
                if article.pdf_url:
                    st.markdown(f"[📄 PDF İndir]({article.pdf_url})")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    except Exception as e:
        show_error_message(f"Makale gösterilirken hata: {str(e)}")


def home_page():
    """Render the home page with article listings."""
    st.title("📚 arXiv'de Güncel Makine Öğrenmesi Makaleleri")
    
    # Sidebar filters
    st.sidebar.markdown("### ⚙️ Filtreler")
    
    max_results = st.sidebar.number_input(
        "Gösterilecek Makale Sayısı", 
        min_value=1, 
        max_value=100, 
        value=10
    )
    
    sort_by = st.sidebar.selectbox(
        "Sıralama Kriteri", 
        ["Yeniden Eskiye", "Eskiden Yeniye"]
    )
    
    # Date range filter
    start_date = st.sidebar.date_input(
        "Başlangıç Tarihi", 
        datetime.now() - timedelta(days=30)
    )
    end_date = st.sidebar.date_input(
        "Bitiş Tarihi", 
        datetime.now()
    )
    
    # Validate date range
    if not validate_date_range(start_date, end_date):
        show_error_message("Başlangıç tarihi bitiş tarihinden sonra olamaz!")
        return
    
    # Search button
    if st.sidebar.button("🔍 Makaleleri Getir", use_container_width=True):
        with st.spinner("Makaleler yükleniyor..."):
            try:
                articles = arxiv_client.fetch_articles(
                    query="cat:cs.LG",
                    max_results=max_results,
                    sort_by=sort_by,
                    start_date=datetime.combine(start_date, datetime.min.time()),
                    end_date=datetime.combine(end_date, datetime.max.time())
                )
                st.session_state.articles = articles
                
                if articles:
                    show_success_message(f"{len(articles)} makale bulundu!")
                else:
                    show_info_box("Belirtilen kriterlere uygun makale bulunamadı.")
            except Exception as e:
                show_error_message(f"Makaleler yüklenirken hata: {str(e)}")
    
    # Display articles
    if st.session_state.articles:
        st.write(f"**{len(st.session_state.articles)}** adet makale gösteriliyor:")
        
        for i, article in enumerate(st.session_state.articles):
            render_article_card(article, index=i)
    else:
        show_info_box("Makale görmek için yukarıdaki filtreleri ayarlayın ve 'Makaleleri Getir' butonuna tıklayın.")


def machine_learning_page():
    """Render the Machine Learning page."""
    st.title("🤖 Makine Öğrenmesi")
    
    st.markdown("""
    <div class="info-box">
        <h3>Makine Öğrenmesi Kategorisi</h3>
        <p>Bu sayfada makine öğrenmesi ile ilgili en güncel arXiv makalelerini bulabilirsiniz.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Subcategory selection
    subcategory = st.selectbox(
        "Alt Kategori Seçin",
        ["Genel (cs.LG)", "Yapay Zeka (cs.AI)", "Bilgisayarlı Görü (cs.CV)", 
         "Doğal Dil İşleme (cs.CL)", "Sinir Ağları (cs.NE)"]
    )
    
    category_map = {
        "Genel (cs.LG)": "cs.LG",
        "Yapay Zeka (cs.AI)": "cs.AI",
        "Bilgisayarlı Görü (cs.CV)": "cs.CV",
        "Doğal Dil İşleme (cs.CL)": "cs.CL",
        "Sinir Ağları (cs.NE)": "cs.NE"
    }
    
    max_results = st.slider("Makale Sayısı", 5, 50, 10)
    
    if st.button("🔍 Makaleleri Getir", use_container_width=True):
        with st.spinner("Makaleler yükleniyor..."):
            try:
                articles = arxiv_client.search_by_category(
                    category=category_map[subcategory],
                    max_results=max_results
                )
                
                if articles:
                    show_success_message(f"{len(articles)} makale bulundu!")
                    for i, article in enumerate(articles):
                        render_article_card(article, index=f"ml_{i}")
                else:
                    show_info_box("Makale bulunamadı.")
            except Exception as e:
                show_error_message(f"Hata: {str(e)}")


def transformers_page():
    """Render the Transformers page."""
    st.title("⚡ Transformers")
    
    st.markdown("""
    <div class="info-box">
        <h3>Transformer Mimarisi</h3>
        <p>Transformer modelleri ve uygulamaları hakkında en güncel araştırmaları keşfedin.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search options
    search_type = st.radio(
        "Arama Türü",
        ["Anahtar Kelime", "Popüler Modeller"]
    )
    
    if search_type == "Anahtar Kelime":
        keyword = st.text_input("Anahtar Kelime Girin", "transformer")
        max_results = st.slider("Makale Sayısı", 5, 50, 10)
        
        if st.button("🔍 Ara", use_container_width=True):
            with st.spinner(f"'{keyword}' araması yapılıyor..."):
                try:
                    articles = arxiv_client.search_by_keyword(
                        keyword=keyword,
                        max_results=max_results
                    )
                    
                    if articles:
                        show_success_message(f"{len(articles)} makale bulundu!")
                        for i, article in enumerate(articles):
                            render_article_card(article, index=f"trans_{i}")
                    else:
                        show_info_box("Makale bulunamadı.")
                except Exception as e:
                    show_error_message(f"Hata: {str(e)}")
    
    else:  # Popular models
        model = st.selectbox(
            "Model Seçin",
            ["BERT", "GPT", "T5", "LLAMA", "Vision Transformer", "CLIP"]
        )
        
        max_results = st.slider("Makale Sayısı", 5, 50, 10)
        
        if st.button("🔍 Makaleleri Getir", use_container_width=True):
            with st.spinner(f"{model} makaleleri yükleniyor..."):
                try:
                    articles = arxiv_client.search_by_keyword(
                        keyword=model,
                        max_results=max_results
                    )
                    
                    if articles:
                        show_success_message(f"{len(articles)} makale bulundu!")
                        for i, article in enumerate(articles):
                            render_article_card(article, index=f"model_{i}")
                    else:
                        show_info_box("Makale bulunamadı.")
                except Exception as e:
                    show_error_message(f"Hata: {str(e)}")


def favorites_page():
    """Render the Favorites page."""
    st.title("⭐ Favoriler")
    
    try:
        favorites = db.get_favorites()
        
        if not favorites:
            show_info_box("Henüz favori makaleniz yok. Ana sayfadan makaleleri favorilere ekleyebilirsiniz.")
        else:
            st.write(f"**{len(favorites)}** favori makaleniz var:")
            
            # Category filter
            categories = list(set(fav['category'] for fav in favorites))
            selected_category = st.selectbox(
                "Kategori Filtrele",
                ["Tümü"] + categories
            )
            
            # Filter favorites
            if selected_category != "Tümü":
                favorites = [fav for fav in favorites if fav['category'] == selected_category]
            
            # Display favorites
            for i, fav in enumerate(favorites):
                # Create a mock article object
                class MockArticle:
                    def __init__(self, fav_data):
                        self.entry_id = fav_data['entry_url']
                        self.title = fav_data['title']
                        self.summary = fav_data['summary']
                        self.pdf_url = fav_data['entry_url'].replace('/abs/', '/pdf/')
                        
                        # Create mock authors
                        class MockAuthor:
                            def __init__(self, name):
                                self.name = name
                        
                        self.authors = [MockAuthor(name) for name in fav_data['authors']]
                        
                        # Parse published date
                        try:
                            self.published = datetime.fromisoformat(fav_data['published_date'].replace(' ', 'T'))
                        except:
                            self.published = datetime.now()
                
                article = MockArticle(fav)
                render_article_card(article, index=f"fav_{i}", show_favorite_button=True)
    
    except Exception as e:
        show_error_message(f"Favoriler yüklenirken hata: {str(e)}")


def statistics_page():
    """Render the Statistics page."""
    st.title("📊 İstatistikler")
    
    try:
        favorites = db.get_favorites()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <h2>{len(favorites)}</h2>
                <p>Toplam Favori</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_likes = sum(db.get_like_count(fav['arxiv_id']) for fav in favorites)
            st.markdown(f"""
            <div class="stats-card">
                <h2>{total_likes}</h2>
                <p>Toplam Beğeni</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            categories = len(set(fav['category'] for fav in favorites))
            st.markdown(f"""
            <div class="stats-card">
                <h2>{categories}</h2>
                <p>Farklı Kategori</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Category distribution
        if favorites:
            st.markdown("### 📈 Kategori Dağılımı")
            category_counts = {}
            for fav in favorites:
                cat = fav['category']
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            for category, count in category_counts.items():
                st.write(f"**{category}**: {count} makale")
        
        # Most liked articles
        st.markdown("### 🔥 En Çok Beğenilen Makaleler")
        if favorites:
            favorites_with_likes = [
                (fav, db.get_like_count(fav['arxiv_id'])) 
                for fav in favorites
            ]
            favorites_with_likes.sort(key=lambda x: x[1], reverse=True)
            
            for fav, likes in favorites_with_likes[:5]:
                if likes > 0:
                    st.write(f"**{fav['title']}** - {likes} beğeni")
        else:
            show_info_box("Henüz beğenilen makale yok.")
    
    except Exception as e:
        show_error_message(f"İstatistikler yüklenirken hata: {str(e)}")


# Main app logic
def main():
    """Main application entry point."""
    main_menu()
    
    # Route to appropriate page
    if st.session_state.menu_option == "Ana Sayfa":
        home_page()
    elif st.session_state.menu_option == "Makine Öğrenmesi":
        machine_learning_page()
    elif st.session_state.menu_option == "Transformers":
        transformers_page()
    elif st.session_state.menu_option == "Favoriler":
        favorites_page()
    elif st.session_state.menu_option == "İstatistikler":
        statistics_page()


if __name__ == "__main__":
    main()
=======
def main_menu() -> None:
    st.sidebar.markdown("### Menu")

    if "menu_option" not in st.session_state:
        st.session_state.menu_option = MENU_OPTIONS[0]

    selected_option = st.sidebar.radio(
        "Select a page",
        MENU_OPTIONS,
        index=MENU_OPTIONS.index(st.session_state.menu_option),
        label_visibility="collapsed",
    )
    st.session_state.menu_option = selected_option

    if selected_option == "Home":
        render_social_links()


st.title("📚 Latest Machine Learning Papers on arXiv")

# Session state for favorites and articles
if "favorites" not in st.session_state:
    st.session_state.favorites = []
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
        if sort_by == "Newest to Oldest"
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
        st.error(f"Translation error: {exc}")
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

# Load the menu
main_menu()

# Home view
if st.session_state.menu_option == "Home":
    # User configuration options
    max_results = st.sidebar.number_input(
        "Number of papers to display", min_value=1, max_value=100, value=10
    )
    sort_by = st.sidebar.selectbox(
        "Sort order", ["Newest to Oldest", "Oldest to Newest"]
    )

    # Date range filter
    start_date = st.sidebar.date_input(
        "Start date", datetime.now() - timedelta(days=30)
    )
    end_date = st.sidebar.date_input("End date", datetime.now())

    # Fetch articles from arXiv
    articles = fetch_articles(max_results, sort_by)

    # Filter by date range
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
    st.session_state.favorites = [
        idx for idx in st.session_state.favorites if idx in valid_indices
    ]

    if not articles:
        st.warning("No papers found in the selected date range.")
    else:
        load_custom_css()

        # Display article details
        st.write(f"Displaying **{len(articles)}** papers:")
        for i, result in enumerate(articles):
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)

                # Title
                title = result.title
                if st.button(
                    f"📄 Translate title to Turkish ({i})", key=f"translate_title_{i}"
                ):
                    title = translate_text(title)
                st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)

                # Authors
                st.markdown(
                    f"<h5>👤 Authors: {', '.join(author.name for author in result.authors)}</h5>",
                    unsafe_allow_html=True,
                )

                # Publication date
                published_date = result.published.strftime("%Y-%m-%d %H:%M")
                st.markdown(
                    f"<h5>📅 Publication Date: {published_date}</h5>",
                    unsafe_allow_html=True,
                )

                # Summary
                summary = result.summary
                if st.button(
                    f"📝 Translate summary to Turkish ({i})",
                    key=f"translate_summary_{i}",
                ):
                    summary = translate_text(summary)
                with st.expander("📖 View summary"):
                    st.write(summary)

                # GitHub links
                github_links = re.findall(github_pattern, result.summary)
                if github_links:
                    st.markdown("**💻 GitHub Repository:**")
                    for link in github_links:
                        st.markdown(f"- [{link}]({link})")
                else:
                    st.markdown("**💻 GitHub Repository:** Not found.")

                # Article link
                st.markdown(f"**🔗 Paper Link:** [arXiv]({result.entry_id})")

                # Like button
                if i not in st.session_state.likes:
                    st.session_state.likes[i] = 0

                if i in st.session_state.user_likes:
                    st.button(
                        f"❤️ Liked ({st.session_state.likes[i]})",
                        key=f"liked_{i}",
                        disabled=True,
                    )
                else:
                    if st.button(
                        f"👍 Like ({st.session_state.likes[i]})", key=f"like_{i}"
                    ):
                        st.session_state.likes[i] += 1
                        st.session_state.user_likes.add(i)

                # Add to favorites button
                if st.button(
                    f"⭐ Add to favorites ({i})", key=f"favorite_{i}"
                ):
                    if i not in st.session_state.favorites:
                        st.session_state.favorites.append(i)
                        st.success("Paper added to favorites! 🎉")
                    else:
                        st.info("Paper already in favorites.")

                st.markdown('</div>', unsafe_allow_html=True)

# Favorites view
elif st.session_state.menu_option == "Favorites":
    st.write("## ⭐ Favorites")
    if not st.session_state.favorites:
        st.write("You have not added any favorite papers yet.")
    else:
        for i in sorted(st.session_state.favorites):
            if i < len(st.session_state.articles):  # Ensure the index is valid
                result = st.session_state.articles[i]
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)

                    # Title
                    st.markdown(f"<h3>{result.title}</h3>", unsafe_allow_html=True)

                    # Authors
                    st.markdown(
                        f"<h5>👤 Authors: {', '.join(author.name for author in result.authors)}</h5>",
                        unsafe_allow_html=True,
                    )

                    # Publication date
                    published_date = result.published.strftime("%Y-%m-%d %H:%M")
                    st.markdown(
                        f"<h5>📅 Publication Date: {published_date}</h5>",
                        unsafe_allow_html=True,
                    )

                    # Summary
                    with st.expander("📖 View summary"):
                        st.write(result.summary)

                    # GitHub links
                    github_links = re.findall(github_pattern, result.summary)
                    if github_links:
                        st.markdown("**💻 GitHub Repository:**")
                        for link in github_links:
                            st.markdown(f"- [{link}]({link})")
                    else:
                        st.markdown("**💻 GitHub Repository:** Not found.")

                    # Article link
                    st.markdown(f"**🔗 Paper Link:** [arXiv]({result.entry_id})")

                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning(
                    f"Paper {i} could not be found. Please reload the papers from the Home tab."
                )

# Machine Learning view
elif st.session_state.menu_option == "Machine Learning":
    st.write("## 🤖 Machine Learning")
    st.write("General information about machine learning will appear here.")

# Transformers view
elif st.session_state.menu_option == "Transformers":
    st.write("## ⚡ Transformers")
    st.write("Details about transformer architectures will appear here.")
>>>>>>> 7754dfbb2684360954b29146f332464316a9b4bc

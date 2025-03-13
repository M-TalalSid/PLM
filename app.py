import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide"
)

# File path for saving/loading library data
LIBRARY_FILE = "library.json"

# Initialize session state to store the library if it doesn't exist
if 'library' not in st.session_state:
    st.session_state.library = []
    
    # Load library from file if it exists
    if os.path.exists(LIBRARY_FILE):
        try:
            with open(LIBRARY_FILE, 'r') as file:
                st.session_state.library = json.load(file)
            
            # Migration step: Ensure all books have the "genres" key
            for book in st.session_state.library:
                if "genres" not in book:
                    book["genres"] = []  # Add "genres" key with an empty list as the default value
            
            st.success(f"Library Loaded Successfully From {LIBRARY_FILE}")
        except Exception as e:
            st.error(f"Error Loading Library: {e}")

# Function to save library to file
def save_library():
    try:
        with open(LIBRARY_FILE, 'w') as file:
            json.dump(st.session_state.library, file, indent=4)
        st.success(f"Library Saved Successfully To {LIBRARY_FILE}")
    except Exception as e:
        st.error(f"Error Saving Library: {e}")

# Function to add a book
def add_book(title, author, publication_year, genres, read_status, cover_image=None, rating=0, review=""):
    # Create book dictionary
    book = {
        "title": title,
        "author": author,
        "publication_year": publication_year,
        "genres": genres,
        "read_status": read_status,
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cover_image": cover_image.read() if cover_image else None,
        "rating": rating,
        "review": review
    }
    
    # Add book to library
    st.session_state.library.append(book)
    save_library()
    return True

# Function to edit a book
def edit_book(index, title, author, publication_year, genres, read_status, cover_image=None, rating=0, review=""):
    new_cover = cover_image.read() if cover_image else st.session_state.library[index]["cover_image"]
    st.session_state.library[index].update({
        "title": title,
        "author": author,
        "publication_year": publication_year,
        "genres": genres,
        "read_status": read_status,
        "cover_image": new_cover,
        "rating": rating,
        "review": review
    })
    save_library()
    return True

# Function to remove a book
def remove_book(title):
    initial_length = len(st.session_state.library)
    st.session_state.library = [book for book in st.session_state.library if book["title"].lower() != title.lower()]
    
    if len(st.session_state.library) < initial_length:
        save_library()
        return True
    return False

# Function to search for books
def search_books(query, search_by):
    results = []
    query = query.lower()
    
    for book in st.session_state.library:
        if search_by == "title" and query in book["title"].lower():
            results.append(book)
        elif search_by == "author" and query in book["author"].lower():
            results.append(book)
        elif search_by == "genre" and any(query in genre.lower() for genre in book["genres"]):
            results.append(book)
    
    return results

# Function to get library statistics
def get_statistics():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read_status"])
    
    if total_books > 0:
        percentage_read = (read_books / total_books) * 100
    else:
        percentage_read = 0
        
    return {
        "total_books": total_books,
        "read_books": read_books,
        "percentage_read": percentage_read
    }

# Welcome message with animation
st.markdown("""
<style>
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    .welcome-message {
        animation: fadeIn 2s ease-in-out;
        font-size: 2.5em;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
    }
</style>
<div class="welcome-message">
    Welcome To Your Personal Library Manager!
</div>
""", unsafe_allow_html=True)

# Sidebar for additional options
with st.sidebar:
    st.header("📚 Library Manager")
    st.markdown("Welcome To Your Personal Library ! Manage Your Book Collection With Ease.")
    st.markdown("---")
    st.markdown("### Quick Actions")
    if st.button("📥 Export Library"):
        st.session_state.export_library = True
    if st.button("🔄 Refresh Library"):
        st.rerun()
    st.markdown("---")
    st.markdown("### Social Media Links")
    st.markdown("[GitHub](https://github.com/M-TalalSid)")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/m-talal-shoaib-8b40322b5/)")
    st.markdown("---")
    st.markdown("### App Info")
    st.markdown("Built Using Streamlit")
    st.markdown("Version 1.2.0")

# Main application header
st.title("📚 Personal Library Manager")
st.markdown("Manage Your Personal Book Collection With Ease!")

# Create tabs for different functionalities
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Add Book", "View Library", "Search Books", "Statistics", "Settings", "Edit Books"])

# Tab 1: Add Book
with tab1:
    st.header("Add a New Book")
    
    # Use a form for better control
    with st.form(key='add_book_form', clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Title")
            author = st.text_input("Author")
            publication_year = st.number_input(
                "Publication Year", 
                min_value=1000, 
                max_value=datetime.now().year, 
                value=2023
            )
        
        with col2:
            genres = st.multiselect(
                "Genre", 
                ["Fiction", "Action", "Adventure", "Comedy", "Horror", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery", "Thriller", 
                 "Romance", "Biography", "History", "Science", "Self-Help", "Other"]
            )
            read_status = st.checkbox("Have you read this book?")
            rating = st.slider("Rate this book (1-5 stars)", 1, 5, value=3)
            cover_image = st.file_uploader("Upload Book Cover (Optional)", type=["jpg", "png", "jpeg"])
            review = st.text_area("Add a Review (Optional)")
        
        # Submit button for the form
        submit_button = st.form_submit_button(label="Add Book")
    
    # Handle form submission
    if submit_button:
        if title and author and genres:  # Basic validation
            if add_book(title, author, publication_year, genres, read_status, cover_image, rating, review):
                st.success(f"'{title}' by {author} added successfully!")
        else:
            st.error("Title, Author, and at least one Genre are required fields.")

# Tab 2: View Library
with tab2:
    st.header("Your Book Collection")
    
    if not st.session_state.library:
        st.info("Your Library Is Empty. Add Some Books To Get Started!")
    else:
        # Add filters
        filter_genre = st.selectbox("Filter by Genre", ["All"] + list(set(genre for book in st.session_state.library for genre in book["genres"])))
        filter_status = st.selectbox("Filter by Status", ["All", "Read", "Unread"])
        filter_rating = st.slider("Filter by Rating", 1, 5, (1, 5))
        
        filtered_books = st.session_state.library
        if filter_genre != "All":
            filtered_books = [book for book in filtered_books if filter_genre in book["genres"]]
        if filter_status != "All":
            filtered_books = [book for book in filtered_books if book["read_status"] == (filter_status == "Read")]
        filtered_books = [book for book in filtered_books if filter_rating[0] <= book.get("rating", 0) <= filter_rating[1]]
        
        # Display filtered books
        for book in filtered_books:
            col1, col2 = st.columns([1, 3])
            with col1:
                if book.get("cover_image"):
                    st.image(book["cover_image"], width=100)
                else:
                    st.image("https://via.placeholder.com/100x150?text=No+Cover", width=100)
            with col2:
                st.subheader(book["title"])
                st.markdown(f"**Author:** {book['author']}")
                st.markdown(f"**Year:** {book['publication_year']}")
                st.markdown(f"**Genres:** {', '.join(book['genres'])}")
                st.markdown(f"**Status:** {'✅ Read' if book['read_status'] else '📖 Unread'}")
                st.markdown(f"**Rating:** {'⭐' * book.get('rating', 0)}")
                st.markdown(f"**Review:** {book.get('review', 'No review yet.')}")
                st.markdown(f"**Date Added:** {book['date_added']}")
            st.markdown("---")

# Tab 3: Search Books
with tab3:
    st.header("Search For Books")
    
    search_by = st.radio("Search by:", ["title", "author", "genre"], horizontal=True)
    search_query = st.text_input(f"Enter {search_by} to search:")
    
    if search_query:
        results = search_books(search_query, search_by)
        
        if results:
            st.success(f"Found {len(results)} matching books!")
            
            # Convert results to DataFrame for display
            results_df = pd.DataFrame(results)
            results_df['read_status'] = results_df['read_status'].apply(lambda x: "✅ Read" if x else "📖 Unread")
            
            # Reorder and rename columns for display
            display_results = results_df[['title', 'author', 'publication_year', 'genres', 'read_status']]
            display_results.columns = ['Title', 'Author', 'Year', 'Genres', 'Status']
            
            st.dataframe(display_results, use_container_width=True)
        else:
            st.info(f"No Books Found Matching '{search_query}' in {search_by}.")

# Tab 4: Statistics
with tab4:
    st.header("Library Statistics")
    
    stats = get_statistics()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Books", stats["total_books"])
    
    with col2:
        st.metric("Books Read", stats["read_books"])
    
    with col3:
        st.metric("Percentage Read", f"{stats['percentage_read']:.1f}%")
    
    if stats["total_books"] > 0:
        # Genre Distribution (Pie Chart)
        genre_counts = {}
        for book in st.session_state.library:
            for genre in book["genres"]:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        genre_df = pd.DataFrame({
            'Genre': list(genre_counts.keys()),
            'Count': list(genre_counts.values())
        })
        
        fig = px.pie(genre_df, values='Count', names='Genre', title="Genre Distribution")
        st.plotly_chart(fig, use_container_width=True)
        
        # Publication Year Distribution (Bar Chart)
        year_counts = {}
        for book in st.session_state.library:
            year = book["publication_year"]
            year_counts[year] = year_counts.get(year, 0) + 1
        
        year_df = pd.DataFrame({
            'Year': list(year_counts.keys()),
            'Count': list(year_counts.values())
        }).sort_values('Year')
        
        fig = px.bar(year_df, x='Year', y='Count', title="Publication Year Distribution")
        st.plotly_chart(fig, use_container_width=True)

# Tab 5: Settings
with tab5:
    st.header("Library Settings")
    
    st.subheader("Save/Load Library")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Save Library To File"):
            save_library()
    
    with col2:
        if st.button("Load Library from File"):
            if os.path.exists(LIBRARY_FILE):
                try:
                    with open(LIBRARY_FILE, 'r') as file:
                        st.session_state.library = json.load(file)
                    
                    # Migration step: Ensure all books have the "genres" key
                    for book in st.session_state.library:
                        if "genres" not in book:
                            book["genres"] = []  # Add "genres" key with an empty list as the default value
                    
                    st.success(f"Library Loaded Successfully From {LIBRARY_FILE}")
                except Exception as e:
                    st.error(f"Error Loading Library: {e}")
            else:
                st.error(f"File {LIBRARY_FILE} does not exist.")
    
    st.subheader("Export Library")
    export_format = st.selectbox("Export format:", ["CSV", "JSON", "Excel"])
    
    if st.button("Export Library"):
        if not st.session_state.library:
            st.error("Library Is Empty. Nothing To Export.")
        else:
            if export_format == "CSV":
                df = pd.DataFrame(st.session_state.library)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="library_export.csv",
                    mime="text/csv"
                )
            elif export_format == "JSON":
                json_str = json.dumps(st.session_state.library, indent=4)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name="library_export.json",
                    mime="application/json"
                )
            else:  # Excel
                df = pd.DataFrame(st.session_state.library)
                excel_file = df.to_excel("library_export.xlsx", index=False)
                with open("library_export.xlsx", "rb") as file:
                    st.download_button(
                        label="Download Excel",
                        data=file,
                        file_name="library_export.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
    
    # Remove specific books
    st.subheader("Remove A Book")
    if st.session_state.library:
        book_to_remove = st.selectbox("Select A Book To Semove:", [book["title"] for book in st.session_state.library])
        if st.button("Remove Selected Book"):
            if remove_book(book_to_remove):
                st.success(f"'{book_to_remove}' Removed Successfully!")
            else:
                st.error("Failed To Remove The Book.")
    else:
        st.info("No Books In The Library To Remove.")

# Tab 6: Edit Books
with tab6:
    st.header("Edit Books")
    
    if not st.session_state.library:
        st.info("Your Library Is Empty. Add Some Books To Edit!")
    else:
        # Select book to edit
        book_titles = [book["title"] for book in st.session_state.library]
        selected_title = st.selectbox("Select a book to edit:", book_titles)
        book_index = book_titles.index(selected_title)
        book = st.session_state.library[book_index]
        
        # Form to edit book details
        with st.form(key=f'edit_book_form_{book_index}', clear_on_submit=False):
            col1, col2 = st.columns(2)
            
            with col1:
                new_title = st.text_input("Title", value=book["title"])
                new_author = st.text_input("Author", value=book["author"])
                new_publication_year = st.number_input(
                    "Publication Year",
                    min_value=1000,
                    max_value=datetime.now().year,
                    value=book["publication_year"]
                )
            
            with col2:
                new_genres = st.multiselect(
                    "Genre",
                    ["Fiction", "Action", "Adventure", "Comedy", "Horror", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery", "Thriller",
                     "Romance", "Biography", "History", "Science", "Self-Help", "Other"],
                    default=book["genres"]
                )
                new_read_status = st.checkbox("Have you read this book?", value=book["read_status"])
                new_rating = st.slider("Rate this book (1-5 stars)", 1, 5, value=book.get("rating", 0))
                new_cover_image = st.file_uploader("Upload New Book Cover (Optional)", type=["jpg", "png", "jpeg"], key=f"edit_cover_{book_index}")
                new_review = st.text_area("Add a Review (Optional)", value=book.get("review", ""))
            
            # Submit button for editing
            submit_edit = st.form_submit_button(label="Update Book")
        
        # Handle form submission for editing
        if submit_edit:
            if new_title and new_author and new_genres:  # Basic validation
                if edit_book(book_index, new_title, new_author, new_publication_year, new_genres, new_read_status, new_cover_image, new_rating, new_review):
                    st.success(f"'{new_title}' by {new_author} updated successfully!")
            else:
                st.error("Title, Author, and at least one Genre are required fields.")

# Auto-save library when the app is closed
def auto_save():
    save_library()

# Register the auto-save function to run when the app is closed
st.session_state.on_close = auto_save
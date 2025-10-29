Movies Recommender Sysytem
# 🎬 Movie Recommendation System

A content-based movie recommendation system built with **Streamlit** and **TMDB API** that suggests similar movies and provides direct access to their trailers.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- 🎯 **Smart Recommendations** - Content-based filtering using cosine similarity
- 🖼️ **Movie Posters** - High-quality posters fetched from TMDB
- ▶️ **YouTube Trailers** - Direct links to official movie trailers
- ⚡ **Fast Performance** - Parallel API calls for optimal speed
- 🎨 **Modern UI** - Clean, responsive interface built with Streamlit

## 🚀 Demo

![Demo Screenshot](home.png)



## 🛠️ Technologies Used

- **Python 3.8+**
- **Streamlit** - Web framework
- **Pandas** - Data manipulation
- **Scikit-learn** - Machine learning (cosine similarity)
- **TMDB API** - Movie data and posters
- **Pickle** - Model serialization

## 📋 Prerequisites

- Python 3.8 or higher
- TMDB API Key ([Get it here](https://www.themoviedb.org/settings/api))

## ⚙️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/movie-recommender.git
cd movie-recommender
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Add your TMDB API Key**
   - Open `app.py`
   - Replace `API_KEY` with your key:
   ```python
   API_KEY = "your_api_key_here"
   ```

5. **Run the application**
```bash
streamlit run app.py
```

## 📁 Project Structure

```
movie-recommender/
│
├── app.py                      # Main Streamlit application
├── artificates/
│   ├── movie_list.pkl          # Preprocessed movie data
│   └── similarity.pkl          # Cosine similarity matrix
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── screenshot.png              # Demo screenshot
```

## 🔧 How It Works

1. **Data Processing**: Movie metadata is preprocessed and converted into feature vectors
2. **Similarity Calculation**: Cosine similarity is computed between all movies
3. **Recommendation**: When a user selects a movie, the system finds the top 5 most similar movies
4. **API Integration**: Movie posters and trailers are fetched in parallel from TMDB API

## 📊 Dataset

The project uses movie data from [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) available on Kaggle.

## 🎯 Future Enhancements

- [ ] Add user ratings and reviews
- [ ] Implement collaborative filtering
- [ ] Genre-based filtering
- [ ] User authentication and favorites
- [ ] Deploy to Streamlit Cloud
- [ ] Add movie search functionality

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Name](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

## 🙏 Acknowledgments

- [TMDB](https://www.themoviedb.org/) for providing the API
- [Streamlit](https://streamlit.io/) for the amazing framework
- Dataset from [Kaggle](https://www.kaggle.com/)

## 📸 Screenshots

### Home Page
![Home](home.png)

### Recommendations
![Recommendations](recommendations.png)

---

⭐ If you found this project helpful, please give it a star!

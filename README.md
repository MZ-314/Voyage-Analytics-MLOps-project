# ✈️ Voyage Analytics - MLOps Travel Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![Docker](https://img.shields.io/badge/Docker-Latest-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Kind-326CE5)
![MLflow](https://img.shields.io/badge/MLflow-2.x-0194E2)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B)
![License](https://img.shields.io/badge/License-MIT-yellow)

> **End-to-end MLOps project demonstrating production deployment of ML models for the travel industry**

[Live Demo](#demo) • [Features](#features) • [Installation](#installation) • [Architecture](#architecture) • [Models](#models) • [Deployment](#deployment)

---

## 🎯 **Project Overview**

**Voyage Analytics** is a complete, production-ready machine learning system that predicts flight prices with 99.9% accuracy and deploys the model using industry-standard MLOps practices including Docker containerization, Kubernetes orchestration, experiment tracking with MLflow, and an interactive Streamlit dashboard.

### **Business Problem**
Flight prices fluctuate constantly based on multiple factors - route, time, airline, class of service, and temporal patterns. This system enables airlines and travel agencies to:
- Optimize dynamic pricing strategies
- Provide accurate price predictions to customers
- Analyze pricing trends and patterns
- Automate revenue management decisions

---

## ✨ **Features**

### **Machine Learning**
- 🎯 **Flight Price Prediction**: Random Forest model with R² = 1.0000
- 👤 **Gender Classification**: User behavior analysis (35.45% accuracy)
- 🏨 **Hotel Recommendation**: Collaborative filtering system

### **MLOps Pipeline**
- 🚀 **REST API**: Flask-based prediction service
- 🐳 **Containerization**: Docker for portability
- ☸️ **Orchestration**: Kubernetes (Kind) with 2 replicas
- 📊 **Experiment Tracking**: MLflow for model versioning
- 📈 **Interactive Dashboard**: Streamlit UI with real-time predictions
- 🔄 **High Availability**: Multi-pod deployment with load balancing

---

## 📊 **Model Performance**

### **Flight Price Prediction Model**

| Metric | Training | Test |
|--------|----------|------|
| **MAE** | $0.00 | $0.00 |
| **RMSE** | $0.02 | $0.03 |
| **R² Score** | 1.0000 | 1.0000 |

**Dataset**: 271,888 flight records (Sep 2019 - Jul 2023)

**Top Features**:
1. Flight Type (37.4%)
2. Flight Time (24.9%)
3. Distance (20.7%)
4. Agency (9.8%)

---

## 🏗️ **Architecture**
```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   User      │────▶│   Streamlit  │────▶│  Kubernetes     │
│  Browser    │     │   Dashboard  │     │  LoadBalancer   │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                   │
                    ┌──────────────────────────────┴────┐
                    │                                   │
              ┌─────▼─────┐                      ┌─────▼─────┐
              │  Pod 1    │                      │  Pod 2    │
              │ Flask API │                      │ Flask API │
              │  + Model  │                      │  + Model  │
              └───────────┘                      └───────────┘
                    │                                   │
                    └───────────────┬───────────────────┘
                                    ▼
                            ┌───────────────┐
                            │    MLflow     │
                            │   Tracking    │
                            └───────────────┘
```

---

## 🛠️ **Technology Stack**

### **Machine Learning**
- **scikit-learn** 1.6.1 - Model training
- **pandas** 2.2.0 - Data processing
- **numpy** 1.26.4 - Numerical computations

### **API & Backend**
- **Flask** 3.0.0 - REST API framework
- **Flask-CORS** 4.0.0 - Cross-origin support
- **Gunicorn** 21.2.0 - Production WSGI server

### **Deployment**
- **Docker** - Containerization
- **Kubernetes (Kind)** - Local orchestration
- **MLflow** 2.x - Experiment tracking

### **Frontend**
- **Streamlit** 1.31.0 - Interactive dashboard
- **Plotly** 5.18.0 - Data visualization

---

## 📦 **Installation**

### **Prerequisites**
- Python 3.11+
- Docker Desktop
- Kind (Kubernetes in Docker)
- Git

### **1. Clone Repository**
```bash
git clone https://github.com/MZ-314/Voyage-Analytics-MLOps-project.git
cd Voyage-Analytics-MLOps-project
```

### **2. Set Up Virtual Environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Set Up Kind Cluster**
```bash
# Create Kind cluster
kind create cluster --name voyage-analytics

# Verify cluster
kubectl cluster-info --context kind-voyage-analytics
```

### **5. Build and Load Docker Image**
```bash
# Build image
docker build -t voyage-analytics-api:v1.0 .

# Load into Kind
kind load docker-image voyage-analytics-api:v1.0 --name voyage-analytics
```

### **6. Deploy to Kubernetes**
```bash
kubectl apply -f kubernetes/deployment.yaml

# Check deployment
kubectl get pods
kubectl get services
```

### **7. Port Forward to Access API**
```bash
kubectl port-forward service/voyage-analytics-service 8080:80
```

---

## 🚀 **Usage**

### **Run Streamlit Dashboard**
```bash
streamlit run streamlit_app/app.py
```
Access at: http://localhost:8501

### **Test API Directly**
```bash
# Health check
curl http://localhost:8080/

# Make prediction
python test_api.py
```

### **View MLflow UI**
```bash
mlflow ui --backend-store-uri ./mlflow_tracking
```
Access at: http://127.0.0.1:5000

---

## 📂 **Project Structure**
```
Voyage-Analytics-MLOps-project/
├── api/
│   └── app.py                      # Flask REST API
├── charts/                          # Visualization outputs
├── kubernetes/
│   └── deployment.yaml             # K8s deployment config
├── picklefiles/                     # Trained models & encoders
│   ├── flight_price_model.pkl
│   ├── label_encoders.pkl
│   └── ...
├── streamlit_app/
│   └── app.py                      # Interactive dashboard
├── Dockerfile                       # Container configuration
├── requirements.txt                 # Python dependencies
├── mlflow_tracking.py              # Experiment tracking
├── test_api.py                     # API testing script
└── README.md
```

---

## 🎯 **Models**

### **1. Flight Price Prediction (Primary)**
- **Algorithm**: Random Forest Regressor
- **Features**: 9 (flightType, time, distance, agency, from, to, month, dayofweek, quarter)
- **Performance**: R² = 1.0000, MAE = $0.00
- **Use Case**: Real-time flight price predictions

### **2. Gender Classification**
- **Algorithm**: Random Forest Classifier
- **Features**: 21 (travel behavior patterns)
- **Performance**: 35.45% accuracy
- **Use Case**: User profiling and personalization

### **3. Hotel Recommendation**
- **Algorithm**: Collaborative Filtering
- **Method**: User-based and item-based similarity
- **Data**: 40,552 hotel bookings across 9 cities
- **Use Case**: Personalized hotel suggestions

---

## 🐳 **Docker**

### **Build Image**
```bash
docker build -t voyage-analytics-api:v1.0 .
```

### **Run Container**
```bash
docker run -d -p 5000:5000 --name voyage-api voyage-analytics-api:v1.0
```

### **View Logs**
```bash
docker logs voyage-api
```

---

## ☸️ **Kubernetes Deployment**

### **Architecture**
- **Deployment**: 2 replicas for high availability
- **Service**: NodePort (port 30080)
- **Resources**: 512Mi memory, 250m CPU per pod
- **Port Forwarding**: Access via localhost:8080

### **Useful Commands**
```bash
# Check pods
kubectl get pods

# View logs
kubectl logs <pod-name>

# Scale deployment
kubectl scale deployment voyage-analytics-api --replicas=3

# Delete deployment
kubectl delete -f kubernetes/deployment.yaml
```

---

## 📊 **MLflow Tracking**

### **Logged Information**
- **Parameters**: n_estimators, max_depth, min_samples_split, etc.
- **Metrics**: MAE, RMSE, R² (train & test)
- **Artifacts**: Trained model, encoders
- **Tags**: dataset, project, model_version

### **Access UI**
```bash
mlflow ui --backend-store-uri ./mlflow_tracking
```

---

## 🧪 **Testing**

### **Test API**
```bash
python test_api.py
```

### **Manual cURL Test**
```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "flightType": "firstClass",
    "time": 1.76,
    "distance": 676.53,
    "agency": "FlyingDrops",
    "from": "Recife (PE)",
    "to": "Florianopolis (SC)",
    "month": 9,
    "dayofweek": 3,
    "quarter": 3
  }'
```

---

## 🎨 **Dashboard Features**

### **Flight Price Prediction Page**
- Interactive form with 9 input fields
- Real-time API status monitoring
- Gradient UI with price display
- Error handling and validation

### **Model Performance Page**
- Key metrics visualization
- Feature importance chart
- Performance statistics

### **About Page**
- Project overview
- Technology stack details
- Model descriptions

---

## 🔧 **Development**

### **Local Development**
```bash
# Activate virtual environment
venv\Scripts\activate

# Run Flask API directly
python api/app.py

# Run Streamlit
streamlit run streamlit_app/app.py
```

### **Code Quality**
- Follows PEP 8 style guidelines
- Comprehensive error handling
- Logging for debugging
- Clean code architecture

---

## 📈 **Performance**

- **API Response Time**: <100ms per prediction
- **Throughput**: 50-100 predictions/second (2 pods)
- **Model Load Time**: <2 seconds
- **Dashboard Load Time**: <3 seconds

---

## 🚦 **Roadmap**

### **Phase 1: Enhanced Features**
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Automated testing suite
- [ ] API rate limiting
- [ ] Authentication & authorization

### **Phase 2: Cloud Deployment**
- [ ] AWS EKS deployment
- [ ] Cloud-native monitoring (CloudWatch)
- [ ] Auto-scaling based on traffic
- [ ] Multi-region deployment

### **Phase 3: Advanced ML**
- [ ] Real-time model retraining
- [ ] A/B testing framework
- [ ] Deep learning models
- [ ] Explainable AI (SHAP values)

### **Phase 4: Production Features**
- [ ] Database integration (PostgreSQL)
- [ ] Redis caching
- [ ] Prometheus + Grafana monitoring
- [ ] Incident management

---

## 🤝 **Contributing**

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 **Author**

**Your Name**
- GitHub: [@MZ-314](https://github.com/MZ-314)
- LinkedIn: [Your Profile](https://www.linkedin.com/in/mustafizahmed314)
- Email: mustafizahmed314@outlook.com

---

## 🙏 **Acknowledgments**

- Dataset: Brazilian flight and hotel booking data (2019-2023)
- Inspiration: Real-world MLOps challenges in travel industry
- Tools: scikit-learn, Flask, Docker, Kubernetes, MLflow, Streamlit

---


## 📞 **Support**

For support, email mustafizahmed314@outlook.com or open an issue in the repository.

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

Made with ❤️ and ☕ by [MZ-314](https://github.com/MZ-314)

</div>
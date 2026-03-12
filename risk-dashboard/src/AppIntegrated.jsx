import React, { useState, useEffect } from "react";
import PredictionForm from "./components/PredictionForm";
import PredictionResult from "./components/PredictionResult";
import FeatureImportance from "./components/FeatureImportance";
import RiskTimeline from "./components/RiskTimeline";
import { healthCheck } from "./api/apiClient";
import { LayoutDashboard, Users, Activity, Settings, Bell, Search, Menu, AlertCircle, CheckCircle } from "lucide-react";

function AppIntegrated() {
  const [prediction, setPrediction] = useState(null);
  const [apiStatus, setApiStatus] = useState('checking');

  useEffect(() => {
    // Check API health on mount
    const checkAPI = async () => {
      try {
        await healthCheck();
        setApiStatus('connected');
      } catch (error) {
        setApiStatus('disconnected');
        console.error('API health check failed:', error);
      }
    };
    checkAPI();
  }, []);

  const handlePredictionComplete = (result) => {
    setPrediction(result);
  };

  return (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-900">

      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 text-slate-300 flex-shrink-0 hidden md:flex flex-col transition-all duration-300">
        <div className="h-16 flex items-center px-6 border-b border-slate-800 bg-slate-950">
          <div className="w-8 h-8 rounded bg-blue-600 flex items-center justify-center mr-3 font-bold text-white">H</div>
          <span className="text-lg font-bold tracking-wide text-white">HEART<span className="text-blue-500">RISK</span></span>
        </div>

        <nav className="flex-1 py-6 px-3 space-y-1">
          <a href="#" className="flex items-center px-3 py-2.5 bg-blue-600 text-white rounded-lg shadow-md transition-all group">
            <LayoutDashboard size={20} className="mr-3" />
            <span className="font-medium">Dashboard</span>
          </a>
          <a href="#" className="flex items-center px-3 py-2.5 hover:bg-slate-800 text-slate-400 hover:text-white rounded-lg transition-all group">
            <Users size={20} className="mr-3" />
            <span className="font-medium">Patients</span>
          </a>
          <a href="#" className="flex items-center px-3 py-2.5 hover:bg-slate-800 text-slate-400 hover:text-white rounded-lg transition-all group">
            <Activity size={20} className="mr-3" />
            <span className="font-medium">Analytics</span>
          </a>
          <a href="#" className="flex items-center px-3 py-2.5 hover:bg-slate-800 text-slate-400 hover:text-white rounded-lg transition-all group">
            <Settings size={20} className="mr-3" />
            <span className="font-medium">Settings</span>
          </a>
        </nav>

        <div className="p-4 border-t border-slate-800">
          <div className="bg-slate-800 rounded-lg p-3">
            <p className="text-xs text-slate-400 mb-1">API Status</p>
            <div className="flex items-center">
              {apiStatus === 'connected' ? (
                <>
                  <CheckCircle size={16} className="text-green-500 mr-2" />
                  <span className="text-sm font-semibold text-green-400">Connected</span>
                </>
              ) : apiStatus === 'disconnected' ? (
                <>
                  <AlertCircle size={16} className="text-red-500 mr-2" />
                  <span className="text-sm font-semibold text-red-400">Disconnected</span>
                </>
              ) : (
                <>
                  <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mr-2"></div>
                  <span className="text-sm font-semibold text-blue-400">Checking...</span>
                </>
              )}
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">

        {/* Top Header */}
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-4 md:px-8 shadow-sm z-10">
          <div className="flex items-center text-slate-500">
            <Menu className="w-6 h-6 mr-4 md:hidden cursor-pointer hover:text-slate-800" />
            <h2 className="text-lg font-semibold text-slate-800 hidden sm:block">Heart Risk Prediction System</h2>
          </div>

          <div className="flex items-center space-x-4">
            <div className="relative hidden md:block">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search patient ID..."
                className="pl-10 pr-4 py-1.5 rounded-full bg-slate-100 border-none focus:ring-2 focus:ring-blue-500 text-sm w-64 transition-all"
              />
            </div>
            <button className="relative p-2 rounded-full hover:bg-slate-100 transition-colors text-slate-500">
              <Bell className="w-5 h-5" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border border-white"></span>
            </button>
            <div className="w-9 h-9 rounded-full bg-blue-100 border border-blue-200 flex items-center justify-center text-blue-700 font-bold text-sm cursor-pointer hover:bg-blue-200 transition-colors">
              DR
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="flex-1 overflow-y-auto p-4 md:p-8">
          <div className="max-w-7xl mx-auto space-y-6">

            {/* Welcome Section */}
            <div className="mb-6">
              <h1 className="text-2xl font-bold text-slate-800">AI-Powered Heart Risk Assessment</h1>
              <p className="text-slate-500 mt-1">Predict cardiovascular risk for radiotherapy patients using machine learning.</p>
            </div>

            {/* API Status Alert */}
            {apiStatus === 'disconnected' && (
              <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
                <div className="flex items-center">
                  <AlertCircle className="text-red-500 mr-3" size={20} />
                  <div>
                    <p className="text-sm font-semibold text-red-800">Backend API Disconnected</p>
                    <p className="text-xs text-red-600 mt-1">
                      Please ensure the backend server is running at http://localhost:8000
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Main Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              
              {/* Left Column: Prediction Form */}
              <div>
                <PredictionForm onPredictionComplete={handlePredictionComplete} />
              </div>

              {/* Right Column: Prediction Result */}
              <div>
                <PredictionResult prediction={prediction} />
              </div>

            </div>

            {/* Bottom Row: Additional Visualizations */}
            {prediction && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
                
                {/* Feature Importance */}
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col h-[300px]">
                  <div className="p-5 border-b border-slate-100">
                    <h3 className="text-lg font-bold text-slate-800">Risk Factor Analysis</h3>
                    <p className="text-sm text-slate-500">Key features driving the prediction model.</p>
                  </div>
                  <div className="flex-1 p-6">
                    <FeatureImportance data={prediction.feature_importance} />
                  </div>
                </div>

                {/* Risk Timeline */}
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col h-[300px]">
                  <div className="p-5 border-b border-slate-100">
                    <h3 className="text-lg font-bold text-slate-800">Risk Progression</h3>
                    <p className="text-sm text-slate-500">Historical risk assessment timeline.</p>
                  </div>
                  <div className="flex-1 p-6">
                    <RiskTimeline />
                  </div>
                </div>

              </div>
            )}

          </div>
        </main>
      </div>
    </div>
  );
}

export default AppIntegrated;

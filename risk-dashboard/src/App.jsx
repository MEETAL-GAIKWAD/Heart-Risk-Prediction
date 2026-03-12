
import React, { useState, useEffect } from "react";
import PatientPanel from "./components/PatientPanel";
import RiskChart from "./components/RiskChart";
import FeatureImportance from "./components/FeatureImportance";
import RiskTimeline from "./components/RiskTimeline";
import AlertsPanel from "./components/AlertsPanel";
import { fetchPatientData } from "./api/mockData";
import { LayoutDashboard, Users, Activity, Settings, Bell, Search, Menu, TrendingUp } from "lucide-react";

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activePatient, setActivePatient] = useState(null);

  useEffect(() => {
    // Initial fetch
    const loadData = async () => {
      setLoading(true);
      const res = await fetchPatientData();
      setData(res);
      setActivePatient(res[0]); // Set first patient as active
      setLoading(false);
    };
    loadData();

    // Live update simulation (every 5 seconds)
    const interval = setInterval(() => {
      setData(prevData => {
        return prevData.map(p => {
          // Randomly adjust risk slightly
          let change = (Math.random() * 6) - 3;
          let newScore = Math.max(0, Math.min(100, p.riskScore + change));

          let newLevel = "Low";
          if (newScore > 75) newLevel = "High";
          else if (newScore > 40) newLevel = "Medium";

          return {
            ...p,
            riskScore: parseFloat(newScore.toFixed(1)),
            riskLevel: newLevel
          };
        });
      });
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  // Update active patient when data changes
  useEffect(() => {
    if (activePatient && data.length > 0) {
      const updated = data.find(p => p.id === activePatient.id);
      if (updated) {
        setActivePatient(updated);
      }
    }
  }, [data]);

  const handleRiskChange = (newRisk) => {
    if (activePatient) {
      const updatedPatient = { ...activePatient, riskScore: newRisk };
      setActivePatient(updatedPatient);
      setData(prevData => prevData.map(p => p.id === activePatient.id ? updatedPatient : p));
    }
  };

  return (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-900">

      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 text-slate-300 flex-shrink-0 hidden md:flex flex-col transition-all duration-300">
        <div className="h-16 flex items-center px-6 border-b border-slate-800 bg-slate-950">
          <div className="w-8 h-8 rounded bg-blue-600 flex items-center justify-center mr-3 font-bold text-white">R</div>
          <span className="text-lg font-bold tracking-wide text-white">RISK<span className="text-blue-500">GUARD</span></span>
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
            <p className="text-xs text-slate-400 mb-1">System Status</p>
            <div className="flex items-center">
              <div className="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></div>
              <span className="text-sm font-semibold text-green-400">Operational</span>
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
            <h2 className="text-lg font-semibold text-slate-800 hidden sm:block">Clinical Risk Assessment</h2>
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
              <h1 className="text-2xl font-bold text-slate-800">Patient Risk Assessment Dashboard</h1>
              <p className="text-slate-500 mt-1">Monitor and predict cardiovascular risk in real-time.</p>
            </div>

            {/* Patient Panel with Risk Meter */}
            {loading ? (
              <div className="h-64 flex items-center justify-center">
                <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
              </div>
            ) : activePatient && (
              <PatientPanel activePatient={activePatient} onRiskChange={handleRiskChange} />
            )}

            {/* Main Visualization Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

              {/* Dose vs Risk Chart (Main) */}
              <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col h-[500px]">
                <div className="p-5 border-b border-slate-100 flex justify-between items-center">
                  <div>
                    <h3 className="text-lg font-bold text-slate-800">Dose vs. Risk Correlation</h3>
                    <p className="text-sm text-slate-500">Real-time analysis across all patients.</p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="flex items-center text-xs font-medium text-slate-500 px-2 py-1 bg-slate-100 rounded-md">
                      <div className="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></div>
                      Live Updates
                    </span>
                  </div>
                </div>
                <div className="flex-1 p-2 md:p-6 w-full overflow-hidden">
                  {loading ? (
                    <div className="h-full flex flex-col items-center justify-center text-slate-400">
                      <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-3"></div>
                      Loading visualization data...
                    </div>
                  ) : (
                    <RiskChart data={data} />
                  )}
                </div>
              </div>

              {/* Alerts Panel */}
              <div className="bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col h-[500px]">
                <div className="p-5 border-b border-slate-100">
                  <h3 className="text-lg font-bold text-slate-800">Active Alerts</h3>
                  <p className="text-sm text-slate-500">Critical notifications & warnings.</p>
                </div>
                <div className="flex-1 overflow-y-auto p-5">
                  <AlertsPanel data={data} />
                </div>
              </div>

            </div>

            {/* Bottom Row: Feature Importance + Risk Timeline */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

              {/* Feature Importance */}
              <div className="bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col h-[300px]">
                <div className="p-5 border-b border-slate-100">
                  <h3 className="text-lg font-bold text-slate-800">Risk Factor Importance</h3>
                  <p className="text-sm text-slate-500">Key features driving the prediction model.</p>
                </div>
                <div className="flex-1 p-6">
                  <FeatureImportance />
                </div>
              </div>

              {/* Risk Progression Timeline */}
              <div className="bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col h-[300px]">
                <div className="p-5 border-b border-slate-100 flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-bold text-slate-800">Risk Progression</h3>
                    <p className="text-sm text-slate-500">
                      {activePatient ? `Timeline for ${activePatient.name}` : 'Patient timeline'}
                    </p>
                  </div>
                  <TrendingUp className="w-5 h-5 text-blue-500" />
                </div>
                <div className="flex-1 p-6">
                  <RiskTimeline patientId={activePatient?.id} />
                </div>
              </div>

            </div>

          </div>
        </main>
      </div>
    </div>
  );
}

export default App;

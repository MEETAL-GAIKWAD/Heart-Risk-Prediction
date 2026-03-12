
import React, { useState } from 'react';
import { User, Activity, Heart, Thermometer, ShieldAlert } from 'lucide-react';
import RiskMeter from './RiskMeter';

const PatientPanel = ({ activePatient, onRiskChange }) => {

    const [patient, setPatient] = useState({
        ...activePatient,
        heartRate: 72,
        cholesterol: 195,
        bp: "120/80"
    });

    // Mock handler for updating risk
    const handleRecalculate = () => {
        // Just mocking a risk recalculation here
        onRiskChange && onRiskChange(Math.floor(Math.random() * 100));
    };

    return (
        <div className="bg-white rounded-xl shadow border border-slate-200 p-6 flex flex-col md:flex-row items-center md:items-start justify-between space-y-6 md:space-y-0 md:space-x-6">

            {/* Left: Patient Info */}
            <div className="w-full md:w-1/3 flex flex-col space-y-4">
                <div className="flex items-center">
                    <div className="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-2xl mr-4 shadow-sm">
                        {patient.name.charAt(0)}
                    </div>
                    <div>
                        <h2 className="text-xl font-bold text-slate-800">{patient.name}</h2>
                        <div className="flex items-center text-sm text-slate-500 mt-1 space-x-2">
                            <span className="bg-slate-100 px-2 py-0.5 rounded text-xs font-mono font-bold">ID: {patient.id}</span>
                            <span>• 54 yrs • Male</span>
                        </div>
                    </div>
                </div>

                <div className="space-y-3 pt-2">
                    <div className="flex items-center justify-between text-sm">
                        <span className="flex items-center text-slate-500"><Heart size={14} className="mr-2 text-red-400" /> Heart Rate</span>
                        <span className="font-semibold text-slate-700">{patient.heartRate} bpm</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                        <span className="flex items-center text-slate-500"><Thermometer size={14} className="mr-2 text-yellow-500" /> Cholesterol</span>
                        <span className="font-semibold text-slate-700">{patient.cholesterol} mg/dL</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                        <span className="flex items-center text-slate-500"><Activity size={14} className="mr-2 text-green-500" /> BP</span>
                        <span className="font-semibold text-slate-700">{patient.bp} mmHg</span>
                    </div>
                </div>

                <button
                    onClick={handleRecalculate}
                    className="mt-4 w-full py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg text-sm shadow-md transition-colors flex items-center justify-center">
                    <ShieldAlert size={16} className="mr-2" /> Recalculate Risk
                </button>
            </div>

            {/* Middle: Live Risk Meter */}
            <div className="w-full md:w-1/3 flex flex-col items-center border-l border-r border-slate-100 px-6">
                <h3 className="text-sm font-bold text-slate-500 uppercase tracking-widest mb-2">Current Risk Level</h3>
                <div className="w-48 h-32">
                    <RiskMeter riskScore={patient.riskScore} />
                </div>
                <div className="mt-2 text-center text-xs text-slate-400">
                    <p>Updated: Just now</p>
                    <p>Model Confidence: 92%</p>
                </div>
            </div>

            {/* Right: Quick Upload / Input */}
            <div className="w-full md:w-1/3 flex flex-col space-y-4">
                <h3 className="text-sm font-semibold text-slate-700 mb-2">Upload New Report</h3>
                <div className="border-2 border-dashed border-slate-200 rounded-lg p-6 flex flex-col items-center justify-center hover:bg-slate-50 hover:border-blue-300 transition-all cursor-pointer">
                    <div className="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center text-blue-500 mb-2">
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                    </div>
                    <p className="text-xs text-slate-500 text-center">Drag & drop or click to upload</p>
                    <p className="text-[10px] text-slate-400 mt-1">Supports PDF, CSV, DICOM</p>
                </div>
                <button className="text-blue-600 text-sm font-semibold hover:underline text-center">
                    Enter data manually
                </button>
            </div>

        </div>
    );
};

export default PatientPanel;

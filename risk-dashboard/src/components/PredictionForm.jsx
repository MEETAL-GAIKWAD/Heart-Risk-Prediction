import React, { useState } from 'react';
import { predictRisk } from '../api/apiClient';
import { AlertCircle, CheckCircle, Loader } from 'lucide-react';

const PredictionForm = ({ onPredictionComplete }) => {
    const [formData, setFormData] = useState({
        age: 45,
        bp: 130,
        cholesterol: 210,
        bmi: 28.5,
        diabetes: 0,
        smoking: 0,
        radiation_dose: 38.0,
        treatment_site: 'left_chest',
        sessions: 25
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    const handleChange = (e) => {
        const { name, value, type } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'number' ? parseFloat(value) : value
        }));
        setError(null);
        setSuccess(false);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setSuccess(false);

        try {
            const result = await predictRisk(formData);
            setSuccess(true);
            if (onPredictionComplete) {
                onPredictionComplete(result);
            }
        } catch (err) {
            setError(err.message || 'Prediction failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
            <h3 className="text-lg font-bold text-slate-800 mb-4">Patient Risk Assessment</h3>
            
            <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Age */}
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">
                            Age (years)
                        </label>
                        <input
                            type="number"
                            name="age"
                            value={formData.age}
                            onChange={handleChange}
                            min="0"
                            max="120"
                            required
                            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>

                    {/* Blood Pressure */}
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">
                            Blood Pressure (mmHg)
                        </label>
                        <input
                            type="number"
                            name="bp"
                            value={formData.bp}
                            onChange={handleChange}
                            min="60"
                            max="200"
                            required
                            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>

                    {/* Cholesterol */}
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">
                            Cholesterol (mg/dL)
                        </label>
                        <input
                            type="number"
                            name="cholesterol"
                            value={formData.cholesterol}
                            onChange={handleChange}
                            min="100"
                            max="400"
                            required
                            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>

                    {/* BMI */}
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">
                            BMI
                        </label>
                        <input
                            type="number"
                            name="bmi"
                            value={formData.bmi}
                            onChange={handleChange}
                            min="10"
                            max="60"
                            step="0.1"
                            required
                            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>

                    {/* Diabetes */}
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">
                            Diabetes
                        </label>
                        <select
                            name="diabetes"
                            value={formData.diabetes}
                            onChange={handleChange}
                            required
                            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                            <option value={0}>No</option>
                            <option value={1}>Yes</option>
                        </select>
                    </div>

                    {/* Smoking */}
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">
                            Smoking
                        </label>
                        <select
                            name="smoking"
                            value={formData.smoking}
                            onChange={handleChange}
                            required
                            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                            <option value={0}>No</option>
                            <option value={1}>Yes</option>
                        </select>
                    </div>

                    {/* Radiation Dose */}
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">
                            Radiation Dose (Gy)
                        </label>
                        <input
                            type="number"
                            name="radiation_dose"
                            value={formData.radiation_dose}
                            onChange={handleChange}
                            min="0"
                            max="100"
                            step="0.1"
                            required
                            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>

                    {/* Treatment Site */}
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">
                            Treatment Site
                        </label>
                        <select
                            name="treatment_site"
                            value={formData.treatment_site}
                            onChange={handleChange}
                            required
                            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                            <option value="left_chest">Left Chest</option>
                            <option value="right_chest">Right Chest</option>
                            <option value="chest">Chest</option>
                            <option value="abdomen">Abdomen</option>
                            <option value="head_neck">Head & Neck</option>
                            <option value="pelvis">Pelvis</option>
                        </select>
                    </div>

                    {/* Sessions */}
                    <div className="md:col-span-2">
                        <label className="block text-sm font-medium text-slate-700 mb-1">
                            Treatment Sessions
                        </label>
                        <input
                            type="number"
                            name="sessions"
                            value={formData.sessions}
                            onChange={handleChange}
                            min="0"
                            max="50"
                            required
                            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                        <AlertCircle size={16} />
                        <span>{error}</span>
                    </div>
                )}

                {/* Success Message */}
                {success && (
                    <div className="flex items-center gap-2 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
                        <CheckCircle size={16} />
                        <span>Prediction completed successfully!</span>
                    </div>
                )}

                {/* Submit Button */}
                <button
                    type="submit"
                    disabled={loading}
                    className="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-400 text-white font-semibold rounded-lg transition-colors flex items-center justify-center gap-2"
                >
                    {loading ? (
                        <>
                            <Loader size={20} className="animate-spin" />
                            <span>Calculating Risk...</span>
                        </>
                    ) : (
                        <span>Calculate Risk</span>
                    )}
                </button>
            </form>
        </div>
    );
};

export default PredictionForm;

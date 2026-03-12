import React from 'react';
import { AlertTriangle, CheckCircle, Info, TrendingUp } from 'lucide-react';
import RiskMeter from './RiskMeter';

const PredictionResult = ({ prediction }) => {
    if (!prediction) {
        return (
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8 text-center">
                <Info size={48} className="mx-auto text-slate-300 mb-4" />
                <p className="text-slate-500">No prediction yet. Fill out the form to calculate risk.</p>
            </div>
        );
    }

    const { risk_probability, risk_level, explanation, feature_importance } = prediction;
    const riskScore = (risk_probability * 100).toFixed(1);

    const getRiskColor = (level) => {
        switch (level) {
            case 'High':
                return 'text-red-600 bg-red-50 border-red-200';
            case 'Medium':
                return 'text-yellow-600 bg-yellow-50 border-yellow-200';
            case 'Low':
                return 'text-green-600 bg-green-50 border-green-200';
            default:
                return 'text-slate-600 bg-slate-50 border-slate-200';
        }
    };

    const getRiskIcon = (level) => {
        switch (level) {
            case 'High':
                return <AlertTriangle size={24} />;
            case 'Medium':
                return <Info size={24} />;
            case 'Low':
                return <CheckCircle size={24} />;
            default:
                return <Info size={24} />;
        }
    };

    return (
        <div className="space-y-6">
            {/* Risk Level Card */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-bold text-slate-800">Risk Assessment Result</h3>
                    <span className="text-xs text-slate-500">
                        {new Date(prediction.timestamp).toLocaleString()}
                    </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Risk Meter */}
                    <div className="flex flex-col items-center">
                        <div className="w-48 h-32 mb-4">
                            <RiskMeter riskScore={parseFloat(riskScore)} />
                        </div>
                        <div className={`px-4 py-2 rounded-lg border-2 font-bold text-lg ${getRiskColor(risk_level)}`}>
                            {getRiskIcon(risk_level)}
                            <span className="ml-2">{risk_level} Risk</span>
                        </div>
                        <p className="text-sm text-slate-500 mt-2">
                            Risk Probability: {(risk_probability * 100).toFixed(1)}%
                        </p>
                    </div>

                    {/* Clinical Explanation */}
                    <div className="flex flex-col justify-center">
                        <h4 className="text-sm font-semibold text-slate-700 mb-2 flex items-center gap-2">
                            <TrendingUp size={16} />
                            Clinical Assessment
                        </h4>
                        <p className="text-sm text-slate-600 leading-relaxed">
                            {explanation}
                        </p>
                    </div>
                </div>
            </div>

            {/* Feature Importance */}
            {feature_importance && (
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                    <h3 className="text-lg font-bold text-slate-800 mb-4">Contributing Factors</h3>
                    <div className="space-y-3">
                        {Object.entries(feature_importance)
                            .sort(([, a], [, b]) => b - a)
                            .slice(0, 6)
                            .map(([feature, importance]) => (
                                <div key={feature} className="flex items-center gap-3">
                                    <div className="w-32 text-sm text-slate-600 capitalize">
                                        {feature.replace(/_/g, ' ')}
                                    </div>
                                    <div className="flex-1 bg-slate-100 rounded-full h-6 overflow-hidden">
                                        <div
                                            className="h-full bg-gradient-to-r from-blue-500 to-blue-600 flex items-center justify-end pr-2"
                                            style={{ width: `${importance * 100}%` }}
                                        >
                                            <span className="text-xs text-white font-semibold">
                                                {(importance * 100).toFixed(1)}%
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            ))}
                    </div>
                </div>
            )}

            {/* Recommendations */}
            <div className={`rounded-xl shadow-sm border-2 p-6 ${getRiskColor(risk_level)}`}>
                <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
                    {getRiskIcon(risk_level)}
                    Recommendations
                </h3>
                <ul className="space-y-2 text-sm">
                    {risk_level === 'High' && (
                        <>
                            <li>• Immediate cardiology consultation recommended</li>
                            <li>• Consider cardiac imaging (echocardiogram, stress test)</li>
                            <li>• Aggressive risk factor modification required</li>
                            <li>• Close cardiovascular monitoring essential</li>
                        </>
                    )}
                    {risk_level === 'Medium' && (
                        <>
                            <li>• Regular cardiovascular monitoring advised</li>
                            <li>• Lifestyle modifications recommended</li>
                            <li>• Follow-up assessment in 3-6 months</li>
                            <li>• Consider preventive medications</li>
                        </>
                    )}
                    {risk_level === 'Low' && (
                        <>
                            <li>• Continue routine cardiovascular surveillance</li>
                            <li>• Maintain healthy lifestyle habits</li>
                            <li>• Annual check-ups recommended</li>
                            <li>• Monitor for any symptom changes</li>
                        </>
                    )}
                </ul>
            </div>
        </div>
    );
};

export default PredictionResult;

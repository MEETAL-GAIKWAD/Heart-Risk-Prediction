
import React from 'react';
import { AlertCircle, AlertTriangle, Info } from 'lucide-react';

const AlertsPanel = ({ data }) => {
    // Generate alerts from data
    const highRiskPatients = data.filter(p => p.riskLevel === 'High');
    const mediumRiskPatients = data.filter(p => p.riskLevel === 'Medium');

    const alerts = [
        ...highRiskPatients.slice(0, 3).map(p => ({
            type: 'critical',
            icon: AlertCircle,
            message: `${p.name} (${p.id}) has critical risk score: ${p.riskScore}`,
            time: 'Just now'
        })),
        {
            type: 'warning',
            icon: AlertTriangle,
            message: `${mediumRiskPatients.length} patients in medium risk category`,
            time: '5 min ago'
        },
        {
            type: 'info',
            icon: Info,
            message: 'Weekly risk assessment report is ready',
            time: '1 hour ago'
        }
    ];

    return (
        <div className="space-y-3">
            {alerts.map((alert, idx) => {
                const Icon = alert.icon;
                let bgColor = 'bg-blue-50';
                let textColor = 'text-blue-600';
                let borderColor = 'border-blue-200';

                if (alert.type === 'critical') {
                    bgColor = 'bg-red-50';
                    textColor = 'text-red-600';
                    borderColor = 'border-red-200';
                } else if (alert.type === 'warning') {
                    bgColor = 'bg-yellow-50';
                    textColor = 'text-yellow-600';
                    borderColor = 'border-yellow-200';
                }

                return (
                    <div key={idx} className={`${bgColor} ${borderColor} border-l-4 p-3 rounded-r-lg hover:shadow-sm transition-shadow`}>
                        <div className="flex items-start">
                            <Icon className={`${textColor} w-4 h-4 mr-3 mt-0.5 flex-shrink-0`} />
                            <div className="flex-1">
                                <p className="text-sm text-slate-700 font-medium">{alert.message}</p>
                                <p className="text-xs text-slate-500 mt-1">{alert.time}</p>
                            </div>
                        </div>
                    </div>
                );
            })}
        </div>
    );
};

export default AlertsPanel;

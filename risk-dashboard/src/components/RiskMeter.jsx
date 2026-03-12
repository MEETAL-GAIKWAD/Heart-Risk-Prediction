
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

const RiskMeter = ({ riskScore }) => {
    // Normalize risk score to 0-100
    const score = Math.min(100, Math.max(0, riskScore));

    const data = [
        { name: 'Risk', value: score },
        { name: 'Remaining', value: 100 - score }
    ];

    let color = '#22c55e'; // Green (Low)
    let label = 'Low Risk';

    if (score > 75) {
        color = '#ef4444'; // Red (High)
        label = 'High Risk';
    } else if (score > 40) {
        color = '#eab308'; // Yellow (Medium)
        label = 'Medium Risk';
    }

    return (
        <div className="relative w-full h-48 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                    <Pie
                        data={data}
                        cx="50%"
                        cy="50%"
                        startAngle={180}
                        endAngle={0}
                        innerRadius={60}
                        outerRadius={80}
                        paddingAngle={5}
                        dataKey="value"
                        stroke="none"
                    >
                        <Cell key="risk" fill={color} cornerRadius={10} />
                        <Cell key="remaining" fill="#e2e8f0" />
                    </Pie>
                </PieChart>
            </ResponsiveContainer>
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-0 text-center mt-2">
                <span className="text-3xl font-bold block" style={{ color: color }}>{score}</span>
                <span className="text-xs font-semibold text-slate-500 uppercase tracking-widest">{label}</span>
            </div>
        </div>
    );
};

export default RiskMeter;

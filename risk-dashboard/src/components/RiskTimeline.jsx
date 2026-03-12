
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';

const RiskTimeline = ({ patientId }) => {
    // Mock timeline data showing risk progression over time
    const timelineData = [
        { date: 'Jan 1', risk: 25, label: 'Low' },
        { date: 'Jan 15', risk: 28, label: 'Low' },
        { date: 'Feb 1', risk: 35, label: 'Low' },
        { date: 'Feb 15', risk: 42, label: 'Medium' },
        { date: 'Mar 1', risk: 48, label: 'Medium' },
        { date: 'Mar 15', risk: 55, label: 'Medium' },
        { date: 'Apr 1', risk: 62, label: 'Medium' },
        { date: 'Apr 15', risk: 58, label: 'Medium' },
        { date: 'May 1', risk: 52, label: 'Medium' },
        { date: 'May 15', risk: 45, label: 'Medium' },
    ];

    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            const data = payload[0].payload;
            return (
                <div className="bg-slate-800 text-white p-3 rounded shadow-lg text-xs border border-slate-700">
                    <p className="font-semibold">{data.date}</p>
                    <p className="text-slate-300">Risk Score: <span className="font-bold text-blue-400">{data.risk}</span></p>
                    <p className="text-slate-300">Level: <span className={`font-bold ${data.risk > 75 ? 'text-red-400' : data.risk > 40 ? 'text-yellow-400' : 'text-green-400'}`}>{data.label}</span></p>
                </div>
            );
        }
        return null;
    };

    return (
        <div className="w-full h-full">
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={timelineData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <defs>
                        <linearGradient id="riskGradient" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                            <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
                    <XAxis
                        dataKey="date"
                        tick={{ fill: '#64748b', fontSize: 11 }}
                        tickLine={false}
                        axisLine={{ stroke: '#cbd5e1' }}
                    />
                    <YAxis
                        domain={[0, 100]}
                        tick={{ fill: '#64748b', fontSize: 11 }}
                        tickLine={false}
                        axisLine={{ stroke: '#cbd5e1' }}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Area
                        type="monotone"
                        dataKey="risk"
                        stroke="#3b82f6"
                        strokeWidth={2}
                        fill="url(#riskGradient)"
                    />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
};

export default RiskTimeline;

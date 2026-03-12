
import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Label, Cell } from 'recharts';

const RiskChart = ({ data }) => {

    // Custom Tooltip
    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            const d = payload[0].payload;
            return (
                <div className="bg-slate-800 text-white p-3 rounded shadow-lg text-sm border border-slate-700 min-w-[200px]">
                    <div className="flex justify-between items-center border-b border-slate-600 pb-2 mb-2">
                        <span className="font-semibold text-lg">{d.id}</span>
                        <span className={`px-2 py-0.5 rounded text-xs font-bold ${d.riskScore > 75 ? 'bg-red-900 text-red-300' : d.riskScore > 40 ? 'bg-yellow-900 text-yellow-300' : 'bg-green-900 text-green-300'}`}>
                            {d.riskLevel.toUpperCase()}
                        </span>
                    </div>
                    <div className="space-y-1">
                        <div className="flex justify-between">
                            <span className="text-slate-400">Dose:</span>
                            <span className="font-mono text-blue-300">{d.dose} mg</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-slate-400">Risk Score:</span>
                            <span className={`font-mono font-bold ${d.riskScore > 75 ? 'text-red-400' : d.riskScore > 40 ? 'text-yellow-400' : 'text-green-400'}`}>
                                {d.riskScore}
                            </span>
                        </div>
                    </div>
                </div>
            );
        }
        return null; // Return null if not active
    };

    return (
        <div style={{ width: '100%', height: '100%', minHeight: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
                <ScatterChart margin={{ top: 20, right: 30, bottom: 20, left: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
                    <XAxis
                        type="number"
                        dataKey="dose"
                        name="Dose"
                        unit=" mg"
                        domain={[0, 'auto']}
                        tick={{ fill: '#64748b', fontSize: 12 }}
                        tickLine={false}
                        axisLine={{ stroke: '#cbd5e1' }}
                        dy={10}
                    >
                        <Label value="Dose Administered (mg)" offset={0} position="insideBottom" style={{ fill: '#475569', fontSize: '12px', fontWeight: 600, dy: 10 }} />
                    </XAxis>
                    <YAxis
                        type="number"
                        dataKey="riskScore"
                        name="Risk Score"
                        domain={[0, 100]}
                        tick={{ fill: '#64748b', fontSize: 12 }}
                        tickLine={false}
                        axisLine={{ stroke: '#cbd5e1' }}
                        dx={-10}
                    >
                        <Label value="Predicted Risk Score" angle={-90} position="insideLeft" style={{ fill: '#475569', fontSize: '12px', fontWeight: 600 }} />
                    </YAxis>
                    <Tooltip content={<CustomTooltip />} cursor={{ strokeDasharray: '3 3' }} />
                    <Scatter name="Patients" data={data} fill="#8884d8">
                        {data.map((entry, index) => {
                            let color = '#22c55e'; // Green
                            if (entry.riskScore > 75) color = '#ef4444'; // Red
                            else if (entry.riskScore > 40) color = '#eab308'; // Yellow

                            return <Cell key={`cell-${index}`} fill={color} strokeWidth={1} stroke="#fff" />;
                        })}
                    </Scatter>
                </ScatterChart>
            </ResponsiveContainer>
        </div>
    );
};

export default RiskChart;

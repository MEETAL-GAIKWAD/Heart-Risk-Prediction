
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const FeatureImportance = ({ data }) => {
    // Default data if none provided
    const defaultData = [
        { name: 'Radiation Dose', value: 85, color: '#3b82f6' },
        { name: 'Age', value: 65, color: '#6366f1' },
        { name: 'BP', value: 55, color: '#8b5cf6' },
        { name: 'Cholesterol', value: 45, color: '#a855f7' },
    ];

    // Convert feature importance object to chart data
    const chartData = data 
        ? Object.entries(data)
            .sort(([, a], [, b]) => b - a)
            .slice(0, 6)
            .map(([name, value], index) => ({
                name: name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
                value: (value * 100).toFixed(1),
                color: ['#3b82f6', '#6366f1', '#8b5cf6', '#a855f7', '#c084fc', '#d8b4fe'][index]
            }))
        : defaultData;

    return (
        <div className="w-full h-full">
            <ResponsiveContainer width="100%" height="100%">
                <BarChart layout="vertical" data={chartData} margin={{ top: 5, right: 30, left: 10, bottom: 5 }}>
                    <XAxis type="number" hide />
                    <YAxis 
                        dataKey="name" 
                        type="category" 
                        width={100} 
                        tick={{ fontSize: 11, fill: '#64748b' }} 
                        tickLine={false} 
                        axisLine={false} 
                    />
                    <Tooltip
                        cursor={{ fill: 'transparent' }}
                        contentStyle={{ 
                            backgroundColor: '#1e293b', 
                            color: '#fff', 
                            border: 'none', 
                            borderRadius: '4px', 
                            fontSize: '12px', 
                            padding: '8px' 
                        }}
                        formatter={(value) => [`${value}%`, 'Importance']}
                    />
                    <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={16}>
                        {chartData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default FeatureImportance;

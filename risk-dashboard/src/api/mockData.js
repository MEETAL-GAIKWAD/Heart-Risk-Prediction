
export const fetchPatientData = () => {
    return new Promise((resolve) => {
        // Simulate network delay
        setTimeout(() => {
            const mockData = Array.from({ length: 30 }, (_, i) => {
                // Generate dose between 10 and 120 mg
                const dose = Math.floor(Math.random() * 110) + 10;

                // Create a correlated risk score
                // Base risk increases with dose, plus some random variation
                let baseRisk = (dose / 120) * 80;
                // Add noise (-15 to +15)
                let noise = (Math.random() * 30) - 15;
                let riskScore = baseRisk + noise;

                // Clamp risk between 0 and 100
                riskScore = Math.min(100, Math.max(0, riskScore));

                let riskLevel = "Low";
                if (riskScore > 75) riskLevel = "High";
                else if (riskScore > 40) riskLevel = "Medium";

                return {
                    id: `P${String(i + 1).padStart(3, '0')}`,
                    name: `Patient ${i + 1}`,
                    dose: dose,
                    riskScore: parseFloat(riskScore.toFixed(1)),
                    riskLevel: riskLevel
                };
            });
            resolve(mockData);
        }, 800);
    });
};

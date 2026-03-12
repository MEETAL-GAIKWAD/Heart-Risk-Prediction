/**
 * API Client for Heart Risk Prediction Backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Predict risk based on patient features
 */
export async function predictRisk(features, patientId = null) {
    try {
        const url = new URL('/predict-risk', API_BASE_URL);
        if (patientId) {
            url.searchParams.append('patient_id', patientId);
        }

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(features),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Prediction failed');
        }

        return await response.json();
    } catch (error) {
        console.error('Error predicting risk:', error);
        throw error;
    }
}

/**
 * Upload medical report (PDF)
 */
export async function uploadReport(file, patientId = null) {
    try {
        const formData = new FormData();
        formData.append('file', file);

        const url = new URL('/upload-report', API_BASE_URL);
        if (patientId) {
            url.searchParams.append('patient_id', patientId);
        }

        const response = await fetch(url, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }

        return await response.json();
    } catch (error) {
        console.error('Error uploading report:', error);
        throw error;
    }
}

/**
 * Get patient history
 */
export async function getPatientHistory(patientId = null, limit = 100) {
    try {
        const url = new URL('/patient-history', API_BASE_URL);
        if (patientId) {
            url.searchParams.append('patient_id', patientId);
        }
        url.searchParams.append('limit', limit);

        const response = await fetch(url);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch history');
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching history:', error);
        throw error;
    }
}

/**
 * Ask AI agent a question
 */
export async function askAgent(question, patientFeatures = null, predictionResult = null) {
    try {
        const response = await fetch(`${API_BASE_URL}/ask-agent`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question,
                patient_features: patientFeatures,
                prediction_result: predictionResult,
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Agent query failed');
        }

        return await response.json();
    } catch (error) {
        console.error('Error asking agent:', error);
        throw error;
    }
}

/**
 * Get statistics
 */
export async function getStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/statistics`);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch statistics');
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching statistics:', error);
        throw error;
    }
}

/**
 * Health check
 */
export async function healthCheck() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);

        if (!response.ok) {
            throw new Error('Health check failed');
        }

        return await response.json();
    } catch (error) {
        console.error('Error in health check:', error);
        throw error;
    }
}

/**
 * Get risk recommendations
 */
export async function getRiskRecommendations(riskLevel) {
    try {
        const url = new URL('/risk-recommendations', API_BASE_URL);
        url.searchParams.append('risk_level', riskLevel);

        const response = await fetch(url);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch recommendations');
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching recommendations:', error);
        throw error;
    }
}

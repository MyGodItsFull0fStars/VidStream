const axios = require('axios');
class RestClient {
    constructor(baseURL) {
        this.client = axios.create({
            baseURL: baseURL,
            headers: { 'Content-Type': 'application/json' },
        });
    }

    async get(url) {
        try {
            const response = await this.client.get(url);
            return response.data;
        } catch (error) {
            console.error(error);
        }
    }

    async post(url, data) {
        try {
            const response = await this.client.post(url, data);
            return response.data;
        } catch (error) {
            console.error(error);
        }
    }

    async put(url, data) {
        try {
            const response = await this.client.put(url, data);
            return response.data;
        } catch (error) {
            console.error(error);
        }
    }

    async delete(url) {
        try {
            const response = await this.client.delete(url);
            return response.data;
        } catch (error) {
            console.error(error);
        }
    }
}

module.exports = RestClient;
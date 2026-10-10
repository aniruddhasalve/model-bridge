export class ModelBridge {
  constructor({ baseUrl, apiKey }) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.apiKey = apiKey;
  }

  async request(path, body) {
    const response = await fetch(`${this.baseUrl}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${this.apiKey}` },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error(`ModelBridge request failed: ${response.status}`);
    return response.json();
  }

  chat(messages) { return this.request('/v1/chat', { messages }); }
  classify(text, labels) { return this.request('/v1/classify', { text, labels }); }
  extract(text, fields) { return this.request('/v1/extract', { text, fields }); }
  summarize(text) { return this.request('/v1/summarize', { text }); }
}

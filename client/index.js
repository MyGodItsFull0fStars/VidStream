/**
 * To start the RESTClient, execute `node index.js` in the terminal
 */

const RestClient = require('./rest-client');

// First try to execute this "entrypoint" file before making any changes to it to see if everything works
// TODO change URL
const API_BASE_URL = 'https://jsonplaceholder.typicode.com';
const client = new RestClient(API_BASE_URL);

// TODO change REST calls to existing calls
(async () => {
    // GET request example
    const posts = await client.get('/posts');
    console.log('GET /posts:', posts);

    // POST request example
    const newPost = {
        title: 'New post title',
        body: 'New post body',
        userId: 1,
    };
    const createdPost = await client.post('/posts', newPost);
    console.log('POST /posts:', createdPost);

    // PUT request example
    const updatedPost = {
        id: 1,
        title: 'Updated post title',
        body: 'Updated post body',
        userId: 1,
    };
    const result = await client.put(`/posts/${updatedPost.id}`, updatedPost);
    console.log(`PUT /posts/${updatedPost.id}:`, result);

    // DELETE request example
    const deletedPost = await client.delete('/posts/1');
    console.log('DELETE /posts/1:', deletedPost);
})();

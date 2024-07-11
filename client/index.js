const serverUrl = 'http://localhost:8080';
const RestClient = require('./rest-client')

const API_BASE_URL = 'http://localhost:8080'
const client = new RestClient(API_BASE_URL);

async function initDummyData(){
    const newPost = {
        title: 'new post title',
        body: 'new post body',
        userId: 1,
    };
    const createdPost = await client.post('/init/{numberOfVideos}', newPost);
    console.log('POST /init/{numberOfVideos}:', newPost);
}

async function getAllVideos(){
    const list = await client.get('/list');
    console.log('GET /list:', list);
}

async function getVideo(){
    const video = await client.get('/find/{id}');
    console.log('GET /find{id}:', video);
}

async function addVideo(){
    const addPostVideo = {
        title: 'new video title',
        body: 'new video body',
        userId: 1,
    };
    const createNewVideo = await client.post('add', addPostVideo);
    console.log('POST /add', addPostVideo)
}
const express = require('express');
const app = express();
const VideoRepository = require('./videoRepository');

app.get('/init/:numberOfVideos', async (req, res) => {
    const numberOfVideos = parseInt(req.params.numberOfVideos, 10);
    let count = 0;

    try {
        const allVideos = await VideoRepository.findAll();
        count = allVideos.length;

        for (let i = 1; i <= numberOfVideos; i++) {
            const video = {
                title: `Video ${count + i}`,
                path: `/tmp/video${count + i}`
            };
            await VideoRepository.save(video);
        }

        res.send('Success');
    } catch (error) {
        res.status(500).send('Error initializing dummy data');
    }
});

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.post('/add', async (req, res) => {
    const { title, path } = req.body;

    try {
        const video = {
            title: title,
            path: path
        };
        await VideoRepository.save(video);

        res.send('add meaningful response');
    } catch (error) {
        res.status(500).send('Error adding video');
    }
});

app.get('/list', async (req, res) => {
    try {
        const allVideos = await VideoRepository.findAll();
        res.json(allVideos);
    } catch (error) {
        res.status(500).send('Error retrieving videos');
    }
});

app.get('/find/:id', async (req, res) => {
    const id = parseInt(req.params.id, 10);

    try {
        const video = await VideoRepository.findById(id);
        if (video) {
            res.json(video);
        } else {
            res.json({ title: "", path: "" });
        }
    } catch (error) {
        res.status(500).send('Error retrieving video');
    }
});





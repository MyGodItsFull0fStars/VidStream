package com.media.mediaserverclient.controller;

import com.media.mediaserverclient.VideoRepository;
import com.media.mediaserverclient.model.Video;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Iterator;

@RestController
public class VideoController {

    @Autowired
    private VideoRepository videoRepository;

    // TODO see https://www.jetbrains.com/help/idea/spring-support-tutorial.html#create-controller

    @GetMapping("/init/{numberOfVideos}")
    public String initDummyData(@PathVariable Integer numberOfVideos) {
        int count = 0;
        for (Video value : videoRepository.findAll()) {
            count++;
        }
        for (int i = 1; i <= numberOfVideos; i++) {
            Video video = new Video();
            video.setTitle("Video " + (count + i));
            video.setPath("/tmp/video" + (count + i));
            videoRepository.save(video);
        }
        return "Success";
    }

    @PostMapping("/add")
    public String addVideo(@RequestParam String title, @RequestParam String path) {

        Video video = new Video();
        video.setTitle(title);
        video.setPath(path);
        videoRepository.save(video);

        return "add meaningful response";
    }

    @GetMapping("/list")
    public Iterable<Video> getAllVideos() {
        return videoRepository.findAll();
    }

    @GetMapping("/find/{id}")
    public Video getVideo(@PathVariable Integer id) {
        return videoRepository.findById(id).orElse(new Video());
    }


//    TODO
//    - getVideos
//    - getVideoById

}



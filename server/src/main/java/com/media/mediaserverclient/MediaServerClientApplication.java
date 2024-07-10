package com.media.mediaserverclient;

import com.media.mediaserverclient.controller.VideoController;
import com.media.mediaserverclient.model.Video;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.service.annotation.GetExchange;

@SpringBootApplication
@RestController
public class MediaServerClientApplication {

    public static void main(String[] args) {
        SpringApplication.run(MediaServerClientApplication.class, args);
    }

    @GetMapping("/hello")
    public String sayHello(@RequestParam(value = "myName", defaultValue = "World") String name) {
        return String.format("Hello %s!", name);
    }

    @GetMapping("/id")
    public String showID(@RequestParam(value = "usr_id", defaultValue = "Please enter a valid user ID") String id) {
        return String.format("%s", id);
    }

    @GetMapping("/userInfo")
    public String getInfo(@RequestParam(value = "usr_id", defaultValue = "Please enter a valid user ID") String id) {
        if (id.equals("1")) {
            return String.format("UserID: %s, Name: Luka", id);
        }
        if (id.equals("2")) {
            return String.format("UserID: %s, Name: Christian", id);
        }
        if (id.equals("3")) {
            return String.format("UserID: %s, Name: Michael", id);
        }
        if (id.equals("4")) {
            return String.format("UserID: %s, Name: David", id);
        }
        if (id.equals("5")) {
            return String.format("UserID: %s, Name: John", id);
        }
        if (id.equals("6")) {
            return String.format("UserID: %s, Name: Jack", id);
        }
        if (id.equals("7")) {
            return String.format("UserID: %s, Name: James", id);
        }
        if (id.equals("8")) {
            return String.format("UserID: %s, Name: Gustavo", id);
        }
        if (id.equals("9")) {
            return String.format("UserID: %s, Name: Walter", id);
        }
        if (id.equals("10")) {
            return String.format("UserID: %s, Name: Jessie", id);
        } else return String.format("Invalid UserID: %s", id);


    }


//    GET VIDEO_LIST

//    VIDEO - name, id

//    GET VIDEO_LIST/id


}


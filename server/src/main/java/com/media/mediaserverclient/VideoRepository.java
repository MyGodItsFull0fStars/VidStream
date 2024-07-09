package com.media.mediaserverclient;

import com.media.mediaserverclient.model.Video;
import org.springframework.data.repository.CrudRepository;

public interface VideoRepository extends CrudRepository<Video, Integer> {

    Video findByVideoId(String videoId);

}

// src/apps/core/data/serializers/BlogPostSerializer.ts
import Serializer from "@/common/serializers/serializer";
import BlogPost from "../models/BlogPost";

export default class BlogPostSerializer extends Serializer<BlogPost, Record<string, any>> {
    
    serialize(instance: BlogPost): Record<string, any> {
        return {
            title: instance.title,
            content: instance.content,
            author: instance.author,
            date: instance.date.toISOString()
        }
    }

    deserialize(data: Record<string, any>): BlogPost {
        return new BlogPost({
            title: data["title"],
            content: data["content"],
            author: data["author"],
            date: new Date(data["date"])
        });
    }
}


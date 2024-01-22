// src/apps/core/data/requests/GetAllBlogPostsRequest.ts
import Request from "@/common/network/Request";
import type BlogPost from "../models/BlogPost";
import BlogPostSerializer from "../serializers/BlogPostSerializer";

export class GetAllBlogPostsRequest extends Request<BlogPost[]> {

    private serializer = new BlogPostSerializer();

    constructor() {
        super({
            url: "/blog",
            method: "GET"
        });
    }

    deserializeResponse(response: any): BlogPost[] {
        return this.serializer.deserializeMany(response);
    }
}


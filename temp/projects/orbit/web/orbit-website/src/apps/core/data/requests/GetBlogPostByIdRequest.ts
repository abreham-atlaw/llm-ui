// src/apps/core/data/requests/GetBlogPostByIdRequest.ts
import Request from "@/common/network/Request";
import type BlogPost from "../models/BlogPost";

export class GetBlogPostByIdRequest extends Request<BlogPost> {

    constructor(id: string) {
        super({
            url: `blog/${id}`,
            method: "GET"
        });
    }
}


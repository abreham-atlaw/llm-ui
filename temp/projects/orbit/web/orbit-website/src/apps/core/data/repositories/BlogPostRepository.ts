// src/apps/core/data/repositories/BlogPostRepository.ts
import CoreProviders from "@/di/coreProviders";
import BlogPost from "../models/BlogPost";
import { GetAllBlogPostsRequest } from "../requests/GetAllBlogPostsRequest";
import { GetBlogPostByIdRequest } from "../requests/GetBlogPostByIdRequest";

export default class BlogPostRepository {
  private networkClient = CoreProviders.provideNetworkClient();

  async getAllBlogPosts(): Promise<BlogPost[]> {
    return await this.networkClient.execute(new GetAllBlogPostsRequest());
  }

  async getBlogPostById(id: string): Promise<BlogPost> {
    return await this.networkClient.execute(new GetBlogPostByIdRequest(id));
  }
}


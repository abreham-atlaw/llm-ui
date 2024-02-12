// src/tests/unit/apps/core/data/BlogPostRepositoryTest.spec.ts

import BlogPost from "@/apps/core/data/models/BlogPost";
import BlogPostRepository from "@/apps/core/data/repositories/BlogPostRepository";
import { beforeEach, describe, test, expect, assertType } from "vitest";

describe(
    "BlogPost Repository Test",
    () => {
        let repo: BlogPostRepository;

        function testBlogPost(blogPost: BlogPost) {
            assertType<BlogPost>(blogPost);
            assertType<string>(blogPost.title);
            assertType<string>(blogPost.content);
            assertType<string>(blogPost.author);
            assertType<Date>(blogPost.date);
        }

        beforeEach(() => {
            repo = new BlogPostRepository();
        })

        test(
            "Get All BlogPosts Test",
            async () => {
                const blogPosts = await repo.getAllBlogPosts();
                assertType<Array<BlogPost>>(blogPosts);
                expect(blogPosts.length).toBeGreaterThan(0);
                for (const blogPost of blogPosts) {
                    testBlogPost(blogPost);
                }
            }
        )

        test(
            "Get BlogPost Test",
            async () => {
                const blogPosts = await repo.getAllBlogPosts();
                if(blogPosts.length === 0){
                    throw Error("Empty BlogPosts");
                }
                const blogPostId = blogPosts[0].id;
                const blogPost = await repo.getBlogPostById(blogPostId);
                testBlogPost(blogPost);
            }
        )
    }
)


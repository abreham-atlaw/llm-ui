import unittest

from llmui.core.agent.directed.sections.implementation.executors.content_check_executor import ContentCheckExecutor
from llmui.di import LLMProviders


class ContentCheckExecutorTest(unittest.TestCase):

	def test_false(self):
		executor = ContentCheckExecutor(LLMProviders.provide_default_llm())

		is_valid = executor((
			"""<template>
  <div>
    <div class="slideshow">
      <div class="slideshow-item" v-for="(image, index) in slideshowImages" :key="index">
        <img :src="image" alt="Slideshow Image" />
      </div>
    </div>
    <h1>Welcome to Orbit</h1>
    <p>Orbit is a leading company providing cutting-edge solutions in Vue3, Typescript, and Ubuntu development.</p>
    <h2>Our Services</h2>
    <ul>
      <li>Vue3 Development</li>
      <li>Typescript Development</li>
      <li>Ubuntu Development</li>
    </ul>
    <button @click="contactUs">Contact Us</button>
    <router-link to="/about">Learn More</router-link>
    <router-link to="/contact">Contact Us</router-link>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import Img0 from '@/assets/images/home/slideshow/01.webp';
import Img1 from '@/assets/images/home/slideshow/02.jpg';
import Img2 from '@/assets/images/home/slideshow/03.webp';

const router = useRouter()

const contactUs = () => {
  router.push('/contact')
}

const slideshowImages = [
  Img0, Img1, Img2
]
</script>

<style scoped>
h1 {
  font-size: 24px;
}

h2 {
  font-size: 18px;
}

ul {
  list-style-type: none;
}

.slideshow {
  position: relative;
  height: 400px;
  overflow: hidden;
}

.slideshow-item {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 0.5s ease-in-out;
}

.slideshow-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.slideshow-item.active {
  opacity: 1;
}

@keyframes slideshow {
  0% {
    opacity: 0;
  }
  20% {
    opacity: 1;
  }
  33% {
    opacity: 1;
  }
  53% {
    opacity: 0;
  }
  100% {
    opacity: 0;
  }
}

.slideshow-item:nth-child(1) {
  animation: slideshow 10s infinite;
}

.slideshow-item:nth-child(2) {
  animation: slideshow 10s infinite 5s;
}

.slideshow-item:nth-child(3) {
  animation: slideshow 10s infinite 10s;
}
</style>

""",

			"Modify the template section to add the desired text on top of the slideshow.",
			"""
			<template>
  <div>
    <div class="slideshow">
      <div class="slideshow-item" v-for="(image, index) in slideshowImages" :key="index">
        <img :src="image" alt="Slideshow Image" />
      </div>
      <div class="slideshow-text">
        <h1>Welcome to Orbit</h1>
        <p>Orbit is a leading company providing cutting-edge solutions in Vue3, Typescript, and Ubuntu development.</p>
      </div>
    </div>
    <h2>Our Services</h2>
    <ul>
      <li>Vue3 Development</li>
      <li>Typescript Development</li>
      <li>Ubuntu Development</li>
    </ul>
    <button @click="contactUs">Contact Us</button>
    <router-link to="/about">Learn More</router-link>
    <router-link to="/contact">Contact Us</router-link>
  </div>
</template>
			"""
		))

		self.assertFalse(is_valid)

	def test_true(self):
		executor = ContentCheckExecutor(LLMProviders.provide_default_llm())

		is_valid = executor((
			"""import { mount } from '@vue/test-utils'
import Header from '@/components/Header.vue'

describe('Header', () => {
  it('renders the app name correctly', () => {
    const wrapper = mount(Header)
    expect(wrapper.find('h1').text()).toBe('Your App Name')
  })

  it('renders the navigation links correctly', () => {
    const wrapper = mount(Header)
    const links = wrapper.findAll('a')
    expect(links.length).toBe(4)
    expect(links[0].text()).toBe('Home')
    expect(links[1].text()).toBe('About')
    expect(links[2].text()).toBe('Services')
    expect(links[3].text()).toBe('Contact')
  })
})
""",

			"Add the import statement for the describe function at the top of the file",
			"""
import { mount } from '@vue/test-utils'
import Header from '@/components/Header.vue'
import { describe } from 'vitest'

describe('Header', () => {
  it('renders the app name correctly', () => {
    const wrapper = mount(Header)
    expect(wrapper.find('h1').text()).toBe('Your App Name')
  })

  it('renders the navigation links correctly', () => {
    const wrapper = mount(Header)
    const links = wrapper.findAll('a')
    expect(links.length).toBe(4)
    expect(links[0].text()).toBe('Home')
    expect(links[1].text()).toBe('About')
    expect(links[2].text()).toBe('Services')
    expect(links[3].text()).toBe('Contact')
  })
})
			"""
		))

		self.assertTrue(is_valid)

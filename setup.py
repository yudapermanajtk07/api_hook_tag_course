from setuptools import setup, find_packages

setup(
    name="api_hook_tag_course",
    version="0.1.0",
    description="Open edX plugin to trigger API on taxonomy/tag changes.",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={
        "lms.djangoapp": [
            "api_hook_tag_course = api_hook_tag_course.apps:ApiHookConfig",
        ],
        "cms.djangoapp": [
            "api_hook_tag_course = api_hook_tag_course.apps:ApiHookConfig",
        ],
    },
)

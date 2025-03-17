from abc import abstractmethod
from typing import Protocol, TypeVar

# Workflow engines / Task orchestration
# https://airflow.apache.org/
# https://github.com/AustralianSynchrotron/Lightflow
# https://github.com/spotify/luigi
# https://luigi.readthedocs.io/en/stable/
# https://docs.openwdl.org/
# https://hevodata.com/learn/build-data-pipeline-python-guide/

# Extract, Transform, and Load
# https://medium.com/@tubelwj/five-common-python-libraries-for-etl-processing-5350a4c1bfeb

# Data pipelines (THIS IS AN ARCHITECTURAL APPROACH FOR THIS!!!)
# https://konfuzio.com/en/python-data-pipeline/#was-ist-eine-datenpipeline-in-python
# https://docs.ploomber.io/en/latest/index.html
# https://medium.com/@iftimiealexandru/data-pipeline-recipes-in-python-8561e07b2556
# https://engineering.nike.com/koheesio/latest/#what-is-koheesio
# https://docs.pydantic.dev/latest/api/experimental/#pydantic.experimental.pipeline
# https://cgarciae.github.io/pypeln/
# https://vmlaker.github.io/mpipe/
# https://vmlaker.github.io/mpipe/cookbook.html | https://joblib.readthedocs.io/en/latest/#
# https://beam.apache.org/get-started/beam-overview/ | https://github.com/apache/beam
# https://beam.apache.org/get-started/quickstart-py/
# https://beam.apache.org/documentation/sdks/yaml/

# https://medium.com/@dkraczkowski/the-elegance-of-modular-data-processing-with-pythons-pipeline-approach-e63bec11d34f
# https://github.com/dkraczkowski/dkraczkowski.github.io/tree/main/articles/crafting-data-processing-pipeline

# https://dagster.io/guides/data-pipeline/data-pipeline-architecture-5-design-patterns-with-examples
# https://medium.com/@bonnotguillaume/software-architecture-the-pipeline-design-pattern-from-zero-to-hero-b5c43d8a4e60
# https://levelup.gitconnected.com/design-patterns-implementing-pipeline-design-pattern-824bd2d42bab

T = TypeVar("T")
TIn = TypeVar("TIn")
TOut = TypeVar("TOut")


class Target:
    pass


class Provider[T](Protocol):
    @abstractmethod
    def get(self) -> T:
        raise NotImplementedError


class Validator[T](Protocol):
    @abstractmethod
    def validate(self, item: T) -> bool:
        raise NotImplementedError


class Transformer[TIn, TOut](Protocol):
    @abstractmethod
    def transform(self, item: TIn) -> TOut:
        raise NotImplementedError

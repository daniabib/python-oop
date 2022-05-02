from __future__ import annotations
from typing import Iterable, Optional
import weakref
import datetime
from typing import List
from math import hypot


class Sample:

    def __init__(
        self,
        sepal_length: float,
        sepal_width: float,
        petal_length: float,
        petal_width: float,
        species: Optional[str] = None
    ) -> None:
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width
        self.species = species
        self.classification: Optional[str] = None

    def __repr__(self) -> str:
        if self.species is None:
            known_unknown = "UnknownSample"
        else:
            known_unknown = "KnownSample"
        if self.classification is None:
            classification = ""
        else:
            classification = f", {self.classification}"
        return (
            f"{known_unknown}("
            f"sepal_length={self.sepal_length}, "
            f"sepal_width={self.sepal_width}, "
            f"petal_length={self.petal_length}, "
            f"petal_width={self.petal_width}, "
            f"species={self.species!r}"
            f"{classification}"
            f")"
        )

    def classify(self, classification: str) -> None:
        self.classification = classification

    def matches(self) -> bool:
        return self.species == self.classification


class Hyperparameter:
    """A hyperparameter value and the overall quality of the
    classification."""

    def __init__(self, k: int, training: "TrainingData") -> None:
        self.k = k
        self.data: weakref.ReferenceType["TrainingData"] = weakref.ref(
            training)

    def test(self) -> None:
        """Run the entire test suite."""
        training_data: Optional["TrainingData"] = self.data()
        if not training_data:
            raise RuntimeError("Broken Weak Reference")
        pass_count, fail_count = 0, 0
        for sample in training_data.testing:
            sample.classification = self.classify(sample)
            if sample.matches():
                pass_count += 1
            else:
                fail_count += 1
        self.quality = pass_count / (pass_count + fail_count)

    def classify(self, sample: Sample) -> str:
        """TODO: the k-nn algorithm"""
        return ""


class TrainingData:
    """A set of training data and testing data with methods to load and
    test the samples."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.upload = datetime.datetime
        self.tested = datetime.datetime
        self.training: List[Sample] = []
        self.testing: List[Sample] = []
        self.tuning: List[Hyperparameter] = []

    def load(
            self,
            raw_data_source: Iterable[dict[str, str]]
    ) -> None:
        """Load and partition the raw data"""
        for n, row in enumerate(raw_data_source):
            """TODO: filter and extract subsets (See Chapter 6)
                     Create self.training and self.testing subsets"""

        self.upload = datetime.datetime.now(tz=datetime.timezone.utc)

    def test(
            self,
            parameter: Hyperparameter) -> None:
        """Test this Hyperparameter value."""
        parameter.test()
        self.tuning.append(parameter)
        self.tested = datetime.datetime.now(tz=datetime.timezone.utc)

    def classify(
            self,
            parameter: Hyperparameter,
            sample: Sample) -> Sample:
        """Classify this Sample."""
        classification = parameter.classify(sample)
        sample.classify(classification)
        return sample


class Distance:
    """Definition of a distance computation"""

    def distance(self, s1: Sample, s2: Sample) -> float:
        pass


class ED(Distance):
    """Computes Euclidean Distance between two samples."""

    def distance(self, s1: Sample, s2: Sample) -> float:
        return hypot(
            s1.sepal_length - s2.sepal_length,
            s1.sepal_width - s2.sepal_width,
            s1.petal_length - s2.petal_length,
            s1.petal_width - s2.petal_width,
        )


class MD(Distance):
    """Computes Manhattan Distance between two samples."""

    def distance(self, s1: Sample, s2: Sample) -> float:
        return sum([
            abs(s1.sepal_length - s2.sepal_length),
            abs(s1.sepal_width - s2.sepal_width),
            abs(s1.petal_length - s2.petal_length),
            abs(s1.petal_width - s2.petal_width),
        ])


class CD(Distance):
    """Computes Chebyshev Distance between two samples."""

    def distance(self, s1: Sample, s2: Sample) -> float:
        return max([
            abs(s1.sepal_length - s2.sepal_length),
            abs(s1.sepal_width - s2.sepal_width),
            abs(s1.petal_length - s2.petal_length),
            abs(s1.petal_width - s2.petal_width),
        ])


class SD(Distance):
    """Computes Sorensen Distance between two samples."""

    def distance(self, s1: Sample, s2: Sample) -> float:
        return sum([
            abs(s1.sepal_length - s2.sepal_length),
            abs(s1.sepal_width - s2.sepal_width),
            abs(s1.petal_length - s2.petal_length),
            abs(s1.petal_width - s2.petal_width),
        ]) / sum([
            s1.sepal_length + s2.sepal_length,
            s1.sepal_width + s2.sepal_width,
            s1.petal_length + s2.petal_length,
            s1.petal_width + s2.petal_width,
        ])


if __name__ == "__main__":
    import time

    s1 = Sample(4.3, 2.1, 1.2, 1.8, "setosa")
    s2 = Sample(2.3, 1.5, 2.5, 2.7, "setosa")
    print(s1)

    ed = ED()
    print(ed.distance(s1, s2))
    md = MD()
    print(md.distance(s1, s2))
    cd = CD()
    print(cd.distance(s1, s2))
    sd = SD()
    print(sd.distance(s1, s2))

    loop_count = 1000000
    start = time.perf_counter()
    for i in range(loop_count):
        ed.distance(s1, s2)
    stop = time.perf_counter()
    print(f"ED time: {stop - start:0.4f} seconds")

    start = time.perf_counter()
    for i in range(loop_count):
        md.distance(s1, s2)
    stop = time.perf_counter()
    print(f"MD time: {stop - start:0.4f} seconds")

    start = time.perf_counter()
    for i in range(loop_count):
        cd.distance(s1, s2)
    stop = time.perf_counter()
    print(f"CD time: {stop - start:0.4f} seconds")
    
    start = time.perf_counter()
    for i in range(loop_count):
        sd.distance(s1, s2)
    stop = time.perf_counter()
    print(f"SD time: {stop - start:0.4f} seconds")
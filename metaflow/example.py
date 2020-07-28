from metaflow import FlowSpec, step, conda_base
from time import sleep

class Flow(FlowSpec):
    """
    Flow Example
    """


    @step
    def start(self):
        """
        Start a flow
        """

        self.next(self.task1, self.task2)

    @step
    def task1(self):
        """
        Task 1
        """
        sleep(30)
        self.next(self.join)

    @step 
    def task2(self):
        """
        Task 2
        """
        sleep(30)
        self.next(self.join)
        
    @step 
    def join(self, inputs):
        """
        Merge tasks 1 and 2
        """

        self.next(self.tunning)

    @step
    def tunning(self):
        """
        Create a list of parameters for tunning
        """
    
        self.parameters = ['A', 'B', 'C']
        self.next(self.parameters_setting, foreach='parameters')

    @step
    def parameters_setting(self):
        """
        Get one parameters and use them in that task
        """

        print(f'Task with value: {self.input}')

        self.next(self.join2)

    @step
    def join2(self, inputs):
        """
        Merge all tunning parameters
        """

        self.next(self.end)
        
    @step
    def end(self):
        """
        End of history
        """
        pass

if __name__ == '__main__':

    Flow()

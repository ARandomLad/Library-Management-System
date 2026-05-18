class Solution(object):
    def maxSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        digit_count = {}
        sub_nums = []
        for i in nums:
            if not i in digit_count:
                digit_count[i] = 0
            digit_count[i] += 1
        for i in digit_count:
            if digit_count[i] >= 1:
                sub_nums.append(i)
        is_positive = False
        for i in sub_nums:
            if i > 0:
                is_positive = True
                break
        if is_positive:
            for i in sub_nums[:]:
                if i < 0:
                    sub_nums.remove(i)
            return sum(sub_nums)
        else:
            return max(sub_nums)

        


solution = Solution()
#Example usage
print(solution.maxSum([1,1,1,1,0,3,4,4,3, 2, 2,-1,-1,-1,-2,-2,-4,-4,-4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]))
print(solution.maxSum([-1, -2, -3, -4, -5]))
print(solution.maxSum([1, 2, 3, 4, 5]))
print(solution.maxSum([-100]))

from math import acos, ceil, floor, cos, sin


class Matrix3:
    def __init__(self):
        self.elements = [
            1, 0, 0,
            0, 1, 0,
            0, 0, 1,
        ]


class Matrix4:
    def __init__(self):
        self.elements = [
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1,
        ]


class Quaternion:
    def __init__(self, x=0, y=0, z=0, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w


_tmp_vector = Vector3()
_tmp_quaternion = Quaternion()

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def setXYZ(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        return self

    def setScalar(self, s):
        self.x = s
        self.y = s
        self.z = s
        return self
    
    def setX(self, x):
        self.x = x
        return self
    
    def setY(self, y):
        self.y = y
        return self

    def setZ(self, z):
        self.z = z
        return self

    def setComponent(self, index, value):
        [self.x, self.y, self.z][index] = value
        return self

    def getComponent(self, index):
        return [self.x, self.y, self.z][index]
    
    def clone(self):
        return Vector3(self.x, self.y, self.z)
    
    def copy(self, v):
        self.x = v.x
        self.y = v.y
        self.z = v.z
        return self
    
    def add(self, v):
        self.x += v.x
        self.y += v.y
        self.z += v.z
        return self
    
    def addScalar(self, s):
        self.x += s
        self.y += s
        self.z += s
        return self
    
    def addVectors(self, a, b):
        self.x = a.x + b.x
        self.y = a.y + b.y
        self.z = a.z + b.z
        return self

    def addScaledVector(self, v, s):
        self.x += v.x * s
        self.y += v.y * s
        self.z += v.z * s
        return self

    def sub(self, v):
        self.x -= v.x
        self.y -= v.y
        self.z -= v.z
        return self

    def subScalar(self, s):
        self.x -= s
        self.y -= s
        self.z -= s
        return self
    
    def subVectors(self, a, b):
        self.x = a.x - b.x
        self.y = a.y - b.y
        self.z = a.z - b.z
        return self
    
    def multiply(self, v):
        self.x *= v.x
        self.y *= v.y
        self.z *= v.z
        return self
    
    def multiplyScalar(self, s):
        self.x *= s
        self.y *= s
        self.z *= s
        return self
    
    def multiplyVectors(self, a, b):
        self.x = a.x * b.x
        self.y = a.y * b.y
        self.z = a.z * b.z
        return self
    
    def applyEuler(self, euler):
        return self.applyQuaternion(_tmp_quaternion.setFromEuler(euler))

    def applyAxisAngle(self, axis, angle):
        return self.applyQuaternion(_tmp_quaternion.setFromAxisAngle(axis, angle))
    
    def applyMatrix3(self, m):
        x, y, z = self.x, self.y, self.z
        e = m.elements

        self.x = e[0] * x + e[3] * y + e[6] * z
		self.y = e[1] * x + e[4] * y + e[7] * z
		self.z = e[2] * x + e[5] * y + e[8] * z
        return self

    def applyNormalMatrix(self, m):
        return self.applyMatrix3(m).normalize()
    
    def applyMatrix4(self, m):
        x, y, z = self.x, self.y, self.z
        e = m.elements

        w = 1 / (e[3] * x + e[7] * y + e[11] * z + e[15])
		self.x = (e[0] * x + e[4] * y + e[8] * z + e[12]) * w
		self.y = (e[1] * x + e[5] * y + e[9] * z + e[13]) * w
		self.z = (e[2] * x + e[6] * y + e[10] * z + e[14]) * w
        return self
    
    def applyQuaternion(self, q):
		x = self.x
        y = self.y
        z = self.z
		qx = q.x
        qy = q.y
        qz = q.z
        qw = q.w

		# calculate quat * vector
		ix = qw * x + qy * z - qz * y
		iy = qw * y + qz * x - qx * z
		iz = qw * z + qx * y - qy * x
		iw = - qx * x - qy * y - qz * z

		# calculate result * inverse quat
		self.x = ix * qw + iw * - qx + iy * - qz - iz * - qy
		self.y = iy * qw + iw * - qy + iz * - qx - ix * - qz
		self.z = iz * qw + iw * - qz + ix * - qy - iy * - qx
		return self

    def project(self, camera):
        return self.applyMatrix4(camera.matrixWorldInverse).applyMatrix4(camera.projectionMatrix)

    def unproject(self, camera):
        return self.applyMatrix4(camera.projectionMatrixInverse).applyMatrix4(camera.matrixWorld)
    
    def transformDirection(self, m: Matrix4):
        # interpret self as directional vector
        # and apply affine transform in matrix4 m
        x = self.x
        y = self.y
        z = self.z
		e = m.elements

		self.x = e[0] * x + e[4] * y + e[8] * z
		self.y = e[1] * x + e[5] * y + e[9] * z
		self.z = e[2] * x + e[6] * y + e[10] * z
		return self.normalize()
    
    def divide(self, v):
        self.x /= v.x
        self.y /= v.y
        self.z /= v.z
        return self

    def divideScalar(self, s):
        self.x /= s
        self.y /= s
        self.z /= s
        return self
    
    def min(self, v):
        self.x = min(self.x, v.x)
        self.y = min(self.y, v.y)
        self.z = min(self.z, v.z)
        return self

    def max(self, v):
        self.x = max(self.x, v.x)
        self.y = max(self.y, v.y)
        self.z = max(self.z, v.z)
        return self
    
    def clamp(self, min_v, max_v):
        # assumes min < max, component-wise
        self.x = max(min_v.x, min(max_v.x, self.x))
        self.y = max(min_v.y, min(max_v.y, self.y))
        self.z = max(min_v.z, min(max_v.z, self.z))
        return self
    
    def clampScalar(self, min_s, max_s):
        self.x = max(min_s, min(max_s, self.x))
        self.y = max(min_s, min(max_s, self.y))
        self.z = max(min_s, min(max_s, self.z))

    def clampLength(self, min_l, max_l):
        l = self.length()
        return self.divideScalar(l or 1).multiplyScalar(max(min_l, min(max_l, l)))

    def floor(self):
        self.x = floor(self.x)
        self.y = floor(self.y)
        self.z = floor(self.z)
        return self
    
    def ceil(self):
        self.x = ceil(self.x)
        self.y = ceil(self.y)
        self.z = ceil(self.z)
        return self
    
    def round(self):
        self.x = round(self.x)
        self.y = round(self.y)
        self.z = round(self.z)
        return self
    
    def roundToZero(self):
        self.x = ceil(self.x) if self.x < 0 else floor(self.x)
        self.y = ceil(self.y) if self.y < 0 else floor(self.y)
        self.z = ceil(self.z) if self.z < 0 else floor(self.z)
        return self
    
    def negate(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self
    
    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def lengthSq(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def length(self):
        return self.lengthSq() ** 0.5

    def manhattanLength(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def normalize(self):
        return self.divideScalar(self.length() or 1)

    def setLength(self, l):
        return self.normalize().multiplyScalar(l)

    def lerp(self, v, a):
        self.x += (v.x - self.x) * a
        self.y += (v.y - self.y) * a
        self.z += (v.z - self.z) * a
        return self
    
    def lerpVectors(self, v1, v2, a):
        return self.subVectors(v2, v1).multiplyScalar(a).add(v1)
    
    def cross(self, v, w):
        return self.crossVectors(self, v)
    
    def crossVectors(self, a, b):
        ax = a.x
        ay = a.y
        az = a.z
		bx = b.x
        by = b.y
        bz = b.z

		self.x = ay * bz - az * by
		self.y = az * bx - ax * bz
		self.z = ax * by - ay * bx
		return self

    def projectOnVector(self, v):
        s = v.dot(self) / v.lengthSq()
        return self.copy(v).multiplyScalar(s)
    
    def projectOnPlane(self, n):
        _tmp_vector.copy(self).projectOnVector(n)
        return self.sub(_tmp_vector)
    
    def reflect(self, n):
        _tmp_vector.copy(n).multiplyScalar(2 * self.dot(n))
        return self.sub(_tmp_vector)
    
    def angleTo(self, v):
        denominator = (self.lenthSq() * v.lengthSq()) ** 0.5
        theta = self.dot(v) / denominator
        return acos(max(-1, min(1, theta)))

    def distanceTo(self, v):
        return self.distanceToSquared(v) ** 0.5
    
    def distanceToSquared(self, v):
        dx = self.x - v.x
        dy = self.y - v.y
        dz = self.z - v.z

		return dx * dx + dy * dy + dz * dz

    def manhattanDistanceTo(self, v):
        return abs(self.x - v.x) + abs(self.y - v.y) + abs(self.z - v.z)
    
    def setFromSpherical(self, s):
        return self.setFromSphericalCoords(s.radius, s.phi, s.theta)
    
    def setFromSphericalCoords(self, radius, phi, theta):
        sin_phi_radius = sin(phi) * radius
		self.x = sin_phi_radius * sin(theta)
		self.y = cos(phi) * radius
		self.z = sin_phi_radius * cos(theta)
		return self

    def setFromCylindrical(self, c):
        return self.setFromCylindricalCoords(c.radius, c.theta, c.y)
    
    def setFromCylindricalCoords(self, radius, theta, y):
        self.x = radius * sin(theta)
        self.y = y
        self.z = radius * cos(theta)
        return self
    
    def setFromMatrixPosition(self, m):
        self.x = m.elements[12]
        self.y = m.elements[13]
        self.z = m.elements[14]
        return self

    def setFromMatrixScale(self, m):
		sx = self.setFromMatrixColumn(m, 0).length()
		sy = self.setFromMatrixColumn(m, 1).length()
		sz = self.setFromMatrixColumn(m, 2).length()

		self.x = sx
		self.y = sy
		self.z = sz
        return self

    def setFromMatrixColumn(self, m, i):
        return self.fromArray(m.elements, i * 4)

    def setFromMatrix3Column(self, m, i):
        return self.fromArray(m.elements, i * 3)

    def equals(self, v):
        return self.x == v.x and self.y == v.y and self.z == v.z
    
    def fromArray(self, array, offset=0):
        self.x = array[offset]
        self.y = array[offset + 1]
        self.z = array[offset + 2]
        return self
    
    def toArray(self, array=None, offset=0):
        if array is None:
            array = []
        
        array[offset] = self.x
        array[offset + 1] = self.y
        array[offset + 2] = self.z
        
        return self
    
    def fromBufferAttribute(self, attribute, index):
        self.x = attribute.getX(index)
        self.y = attribute.getY(index)
        self.z = attribute.getZ(index)
        return self

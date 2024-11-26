# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for IDEs based on JetBrains IntelliJ Platform: IntelliJ IDEA, Android Studio, PyCharm, and others."""

import appModuleHandler
import controlTypes
from NVDAObjects.JAB import JAB, JABTextInfo


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if isinstance(obj, JAB) and obj.role == controlTypes.Role.EDITABLETEXT:
			clsList.insert(0, IntellijJAB)
		return clsList


class IntellijJAB(JAB):
	def _get_TextInfo(self):
		return IntellijJABTextInfo


class IntellijJABTextInfo(JABTextInfo):
	"""
	Extension of the default JAB TextInfo object with an implementation of the getWordOffsets method,
	which improves the reading of separate words in editable text components.
	This method is implemented by querying the boundaries of words from the Java Access Bridge API,
	which may not return correct information for all Java applications,
	so it's done in an app module only for JetBrains IDEs.
	"""

	def _getWordOffsets(self, offset) -> tuple[int, int]:
		# JAB doesn't have an API to get word offsets directly, but we can get the current word as a string.
		word = self.obj.jabContext.getAccessibleTextItems(offset).word
		wordLen = len(word)

		# The word can be on either side of the offset, so search all possible positions.
		for i in range(0, wordLen + 1):
			if self.obj.jabContext.getAccessibleTextRange(offset - i, offset + wordLen - i - 1) == word:
				return offset - i, offset + wordLen - i

		return super(JABTextInfo, self)._getWordOffsets(offset)
